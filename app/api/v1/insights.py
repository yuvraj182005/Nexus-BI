import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.insights.schemas import (
    BusinessInsightResponse,
    WhatIfSimulationRequest,
    WhatIfSimulationResponse,
)
from app.insights.service import InsightsService
from app.models.identity import User, UserRole

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
InsightManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.get("/datasets/{dataset_id}/insights", response_model=list[BusinessInsightResponse])
async def get_insights(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> list[BusinessInsightResponse]:
    try:
        return await InsightsService(session, get_settings()).generate_insights(user, workspace_id, dataset_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/datasets/{dataset_id}/insights/what-if", response_model=WhatIfSimulationResponse)
async def simulate_what_if(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: WhatIfSimulationRequest,
    session: Session,
    user: InsightManager,
) -> WhatIfSimulationResponse:
    try:
        return await InsightsService(session, get_settings()).simulate_what_if(user, workspace_id, dataset_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
