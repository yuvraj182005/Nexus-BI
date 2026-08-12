import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.copilot.schemas import CopilotRequest, CopilotResponse
from app.copilot.service import global_copilot_service
from app.database.session import get_db_session
from app.models.identity import User

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/copilot/execute", response_model=CopilotResponse)
async def execute_copilot(
    workspace_id: uuid.UUID,
    request: CopilotRequest,
    session: Session,
    user: CurrentUser,
) -> CopilotResponse:
    return await global_copilot_service.execute_copilot(user.id, workspace_id, request)
