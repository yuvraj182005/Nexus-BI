import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.notifications.schemas import NotificationSendRequest, NotificationSendResponse
from app.notifications.service import NotificationsService

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
NotifManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.post("/notifications/send", response_model=NotificationSendResponse)
async def send_notification(
    workspace_id: uuid.UUID,
    request: NotificationSendRequest,
    session: Session,
    user: NotifManager,
) -> NotificationSendResponse:
    try:
        return await NotificationsService(session, get_settings()).send_notification(user, workspace_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
