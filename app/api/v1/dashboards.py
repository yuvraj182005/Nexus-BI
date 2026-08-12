import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dashboards.schemas import (
    DashboardCreateRequest,
    DashboardDetailResponse,
    DashboardSnapshotResponse,
)
from app.dashboards.service import global_dashboard_builder
from app.database.session import get_db_session
from app.models.identity import User

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/dashboards/builder", response_model=DashboardDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_builder_dashboard(
    workspace_id: uuid.UUID,
    request: DashboardCreateRequest,
    session: Session,
    user: CurrentUser,
) -> DashboardDetailResponse:
    return global_dashboard_builder.create_dashboard(workspace_id, request)


@router.post("/dashboards/{dashboard_id}/snapshot", response_model=DashboardSnapshotResponse)
async def generate_dashboard_snapshot(
    workspace_id: uuid.UUID,
    dashboard_id: str,
    session: Session,
    user: CurrentUser,
) -> DashboardSnapshotResponse:
    try:
        return global_dashboard_builder.generate_snapshot(dashboard_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/dashboards/{dashboard_id}/bookmarks", response_model=DashboardDetailResponse)
async def add_dashboard_bookmark(
    workspace_id: uuid.UUID,
    dashboard_id: str,
    session: Session,
    user: CurrentUser,
    bookmark_name: str = Body(..., embed=True),
    filter_state: dict[str, Any] = Body(default_factory=dict, embed=True),
) -> DashboardDetailResponse:
    try:
        return global_dashboard_builder.add_bookmark(dashboard_id, bookmark_name, filter_state)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
