import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.visualization.schemas import (
    ChartGenerateRequest,
    ChartGenerateResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from app.visualization.service import VisualizationService

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
VisManager = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))]


@router.post("/datasets/{dataset_id}/visualizations/recommend", response_model=RecommendationResponse)
async def recommend_visualizations(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: RecommendationRequest,
    session: Session,
    user: CurrentUser,
) -> RecommendationResponse:
    try:
        return await VisualizationService(session, get_settings()).recommend(user, workspace_id, dataset_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/datasets/{dataset_id}/visualizations/generate", response_model=ChartGenerateResponse)
async def generate_visualization(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: ChartGenerateRequest,
    session: Session,
    user: VisManager,
) -> ChartGenerateResponse:
    try:
        return await VisualizationService(session, get_settings()).generate_chart(user, workspace_id, dataset_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
