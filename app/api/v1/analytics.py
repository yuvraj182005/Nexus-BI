import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.schemas import EDARequest, EDAResponse
from app.analytics.service import AnalyticsService
from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AnalyticsManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.post("/datasets/{dataset_id}/analytics/eda", response_model=EDAResponse)
async def run_eda(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: EDARequest,
    session: Session,
    user: AnalyticsManager,
) -> EDAResponse:
    try:
        return await AnalyticsService(session, get_settings()).run_eda(user, workspace_id, dataset_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
