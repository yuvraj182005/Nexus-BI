import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.sql_engine.schemas import (
    SQLExecuteRequest,
    SQLExecuteResponse,
    SQLExplainRequest,
    SQLExplainResponse,
    SQLGenerateRequest,
    SQLGenerateResponse,
)
from app.sql_engine.service import SQLService

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
SQLManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.post("/datasets/{dataset_id}/sql/generate", response_model=SQLGenerateResponse)
async def generate_sql(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: SQLGenerateRequest,
    session: Session,
    user: SQLManager,
) -> SQLGenerateResponse:
    try:
        return await SQLService(session, get_settings()).generate_sql(user, workspace_id, dataset_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/datasets/{dataset_id}/sql/execute", response_model=SQLExecuteResponse)
async def execute_sql(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: SQLExecuteRequest,
    session: Session,
    user: SQLManager,
) -> SQLExecuteResponse:
    try:
        return await SQLService(session, get_settings()).execute_sql(user, workspace_id, dataset_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/datasets/{dataset_id}/sql/explain", response_model=SQLExplainResponse)
async def explain_sql(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: SQLExplainRequest,
    session: Session,
    user: CurrentUser,
) -> SQLExplainResponse:
    return await SQLService(session, get_settings()).explain_sql(request)
