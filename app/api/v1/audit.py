import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.audit.schemas import AuditExportResponse, AuditSearchRequest, AuditSearchResponse
from app.audit.service import global_audit_service
from app.auth.dependencies import get_current_user, require_roles
from app.database.session import get_db_session
from app.models.identity import User, UserRole

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AuditAdmin = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))]


@router.post("/audit/search", response_model=AuditSearchResponse)
async def search_audit_logs(
    workspace_id: uuid.UUID,
    request: AuditSearchRequest,
    session: Session,
    user: AuditAdmin,
) -> AuditSearchResponse:
    return await global_audit_service.search_logs(workspace_id, request)


@router.get("/audit/export", response_model=AuditExportResponse)
async def export_audit_logs(
    workspace_id: uuid.UUID,
    session: Session,
    user: AuditAdmin,
    format: str = Query("json", description="json or csv"),
) -> AuditExportResponse:
    return await global_audit_service.export_logs(workspace_id, export_format=format)
