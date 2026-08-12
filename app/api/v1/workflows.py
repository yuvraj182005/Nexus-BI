import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.workflows.schemas import (
    WorkflowExecuteRequest,
    WorkflowExecutionResponse,
    WorkflowTemplate,
)
from app.workflows.service import WorkflowService

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
WorkflowManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.get("/workflows/templates", response_model=list[WorkflowTemplate])
async def list_workflow_templates(
    workspace_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> list[WorkflowTemplate]:
    return await WorkflowService(session, get_settings()).list_templates()


@router.post("/workflows/execute", response_model=WorkflowExecutionResponse)
async def execute_workflow(
    workspace_id: uuid.UUID,
    request: WorkflowExecuteRequest,
    session: Session,
    user: WorkflowManager,
) -> WorkflowExecutionResponse:
    try:
        return await WorkflowService(session, get_settings()).execute_workflow(user, workspace_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
