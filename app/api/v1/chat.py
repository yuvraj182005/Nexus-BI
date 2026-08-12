import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.chat.schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSessionCreateRequest,
    ChatSessionResponse,
)
from app.chat.service import ChatService
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/chat/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    workspace_id: uuid.UUID,
    request: ChatSessionCreateRequest,
    session: Session,
    user: CurrentUser,
) -> ChatSessionResponse:
    return await ChatService(session, get_settings()).create_session(user, workspace_id, request)


@router.post("/chat/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_chat_message(
    workspace_id: uuid.UUID,
    session_id: uuid.UUID,
    request: ChatMessageRequest,
    session: Session,
    user: CurrentUser,
) -> ChatMessageResponse:
    try:
        return await ChatService(session, get_settings()).send_message(user, workspace_id, session_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
