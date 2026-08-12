import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.connectors.base import ConnectorError
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.connector import ConnectorStatus, ConnectorSyncRun, SyncStatus
from app.models.identity import User, UserRole
from app.repositories.connector import ConnectorRepository
from app.schemas.connector import (
    ConnectorCreateRequest,
    ConnectorDiscoveryResponse,
    ConnectorHealthResponse,
    ConnectorResponse,
    ConnectorSyncResponse,
    ConnectorTableResponse,
    ConnectorUpdateRequest,
)
from app.services.connector import ConnectorService
from app.tasks.connector import sync_connector

router = APIRouter(prefix="/workspaces/{workspace_id}/connectors")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ConnectorManager = Annotated[
    User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))
]


async def load_connector(
    session: AsyncSession, user: User, workspace_id: uuid.UUID, connector_id: uuid.UUID
):
    connector = await ConnectorRepository(session).get(connector_id, user, workspace_id)
    if not connector:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connector not found")
    return connector


@router.post("", response_model=ConnectorResponse, status_code=status.HTTP_201_CREATED)
async def create_connector(
    workspace_id: uuid.UUID, request: ConnectorCreateRequest, session: Session, user: ConnectorManager
) -> ConnectorResponse:
    try:
        return await ConnectorService(session, get_settings()).create(user, workspace_id, request)
    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[ConnectorResponse])
async def list_connectors(workspace_id: uuid.UUID, session: Session, user: CurrentUser):
    return await ConnectorRepository(session).list(user, workspace_id)


@router.get("/{connector_id}", response_model=ConnectorResponse)
async def get_connector(
    workspace_id: uuid.UUID, connector_id: uuid.UUID, session: Session, user: CurrentUser
) -> ConnectorResponse:
    return await load_connector(session, user, workspace_id, connector_id)


@router.patch("/{connector_id}", response_model=ConnectorResponse)
async def update_connector(
    workspace_id: uuid.UUID,
    connector_id: uuid.UUID,
    request: ConnectorUpdateRequest,
    session: Session,
    user: ConnectorManager,
) -> ConnectorResponse:
    connector = await load_connector(session, user, workspace_id, connector_id)
    return await ConnectorService(session, get_settings()).update(connector, request)


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disable_connector(
    workspace_id: uuid.UUID, connector_id: uuid.UUID, session: Session, user: ConnectorManager
) -> None:
    connector = await load_connector(session, user, workspace_id, connector_id)
    connector.status = ConnectorStatus.DISABLED
    connector.sync_enabled = False
    await session.commit()


@router.post("/{connector_id}/test", response_model=ConnectorHealthResponse)
async def test_connector(
    workspace_id: uuid.UUID, connector_id: uuid.UUID, session: Session, user: ConnectorManager
) -> ConnectorHealthResponse:
    connector = await load_connector(session, user, workspace_id, connector_id)
    healthy, message, latency = await ConnectorService(session, get_settings()).validate(connector)
    return ConnectorHealthResponse(
        connector_id=connector.id,
        status=ConnectorStatus.HEALTHY if healthy else ConnectorStatus.UNHEALTHY,
        healthy=healthy,
        message=message,
        latency_ms=latency,
    )


@router.get("/{connector_id}/health", response_model=ConnectorHealthResponse)
async def connector_health(
    workspace_id: uuid.UUID, connector_id: uuid.UUID, session: Session, user: CurrentUser
) -> ConnectorHealthResponse:
    connector = await load_connector(session, user, workspace_id, connector_id)
    healthy, message, latency = await ConnectorService(session, get_settings()).validate(connector)
    return ConnectorHealthResponse(
        connector_id=connector.id,
        status=ConnectorStatus.HEALTHY if healthy else ConnectorStatus.UNHEALTHY,
        healthy=healthy,
        message=message,
        latency_ms=latency,
    )


@router.get("/{connector_id}/schema", response_model=ConnectorDiscoveryResponse)
async def discover_connector_schema(
    workspace_id: uuid.UUID, connector_id: uuid.UUID, session: Session, user: CurrentUser
) -> ConnectorDiscoveryResponse:
    connector = await load_connector(session, user, workspace_id, connector_id)
    try:
        tables = await ConnectorService(session, get_settings()).discover_schema(connector)
    except (ConnectorError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return ConnectorDiscoveryResponse(
        connector_id=connector.id,
        tables=[ConnectorTableResponse(name=t.name, columns=t.columns, row_count=t.row_count) for t in tables],
    )


@router.post("/{connector_id}/sync", response_model=ConnectorSyncResponse, status_code=status.HTTP_202_ACCEPTED)
async def sync_connector_data(
    workspace_id: uuid.UUID, connector_id: uuid.UUID, session: Session, user: ConnectorManager
) -> ConnectorSyncResponse:
    connector = await load_connector(session, user, workspace_id, connector_id)
    run = await ConnectorRepository(session).create_run(connector.id)
    await session.commit()
    sync_connector.delay(str(connector.id), str(run.id))
    return ConnectorSyncResponse(
        connector_id=connector.id,
        run_id=run.id,
        status=SyncStatus.RUNNING,
        rows_synced=None,
        error_message=None,
    )


@router.get("/{connector_id}/sync/{run_id}", response_model=ConnectorSyncResponse)
async def get_sync_run(
    workspace_id: uuid.UUID,
    connector_id: uuid.UUID,
    run_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> ConnectorSyncResponse:
    connector = await load_connector(session, user, workspace_id, connector_id)
    run = await session.get(ConnectorSyncRun, run_id)
    if not run or run.connector_id != connector.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sync run not found")
    tables = [
        ConnectorTableResponse(
            name=table["name"],
            columns=table.get("columns", []),
            row_count=table.get("row_count"),
        )
        for table in (run.schema_json or [])
    ]
    return ConnectorSyncResponse(
        connector_id=connector.id,
        run_id=run.id,
        status=run.status,
        rows_synced=run.rows_synced,
        tables=tables,
        error_message=run.error_message,
    )
