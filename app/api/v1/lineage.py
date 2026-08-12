import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db_session
from app.lineage.schemas import ImpactAnalysisResponse, LineageGraphResponse
from app.lineage.service import global_lineage_service
from app.models.identity import User

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/datasets/{dataset_id}/lineage-graph", response_model=LineageGraphResponse)
async def get_dataset_lineage_graph(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> LineageGraphResponse:
    return global_lineage_service.get_lineage_graph(dataset_id)


@router.get("/lineage/impact-analysis", response_model=ImpactAnalysisResponse)
async def get_deletion_impact_analysis(
    workspace_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    object_id: str = Query(..., description="ID of entity targeted for deletion"),
    object_type: str = Query("dataset", description="dataset, dashboard, report, workflow"),
) -> ImpactAnalysisResponse:
    return global_lineage_service.analyze_deletion_impact(object_id, object_type)
