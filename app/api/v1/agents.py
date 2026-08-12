import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import AgentOrchestrator
from app.agents.schemas import AgentWorkflowRequest, AgentWorkflowResponse
from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AgentManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.post("/agents/execute", response_model=AgentWorkflowResponse)
async def execute_agent_workflow(
    workspace_id: uuid.UUID,
    request: AgentWorkflowRequest,
    session: Session,
    user: AgentManager,
) -> AgentWorkflowResponse:
    try:
        return await AgentOrchestrator(session, get_settings()).execute_workflow(user, workspace_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
