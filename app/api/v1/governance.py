import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.governance.schemas import GovernanceAuditResponse, PIIScanResponse
from app.governance.service import GovernanceService
from app.models.identity import User, UserRole

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
GovernanceManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.post("/datasets/{dataset_id}/governance/pii-scan", response_model=PIIScanResponse)
async def scan_dataset_pii(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: GovernanceManager,
) -> PIIScanResponse:
    try:
        return await GovernanceService(session, get_settings()).scan_pii(user, workspace_id, dataset_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/datasets/{dataset_id}/governance/audit", response_model=GovernanceAuditResponse)
async def audit_dataset_governance(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> GovernanceAuditResponse:
    try:
        return await GovernanceService(session, get_settings()).audit_governance(user, workspace_id, dataset_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
