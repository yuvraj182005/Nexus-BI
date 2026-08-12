import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.reports.schemas import ReportGenerateRequest, ReportGenerateResponse
from app.reports.service import ReportsService

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ReportManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.post("/datasets/{dataset_id}/reports/generate", response_model=ReportGenerateResponse)
async def generate_report(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: ReportGenerateRequest,
    session: Session,
    user: ReportManager,
) -> ReportGenerateResponse:
    try:
        return await ReportsService(session, get_settings()).generate_report(user, workspace_id, dataset_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
