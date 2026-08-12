import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db_session
from app.models.identity import User
from app.saas.schemas import InvoiceRecord, WorkspaceUsageDashboard
from app.saas.service import global_saas_service

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/saas/usage", response_model=WorkspaceUsageDashboard)
async def get_saas_usage_dashboard(
    workspace_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> WorkspaceUsageDashboard:
    return global_saas_service.get_workspace_usage(workspace_id)


@router.post("/saas/payment-webhook", response_model=InvoiceRecord)
async def handle_stripe_payment_webhook(
    workspace_id: uuid.UUID,
    event_type: str = Body(..., embed=True),
    amount_usd: float = Body(..., embed=True),
) -> InvoiceRecord:
    return global_saas_service.process_payment_webhook(workspace_id, event_type, amount_usd)
