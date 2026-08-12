import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.repositories.dataset import DatasetRepository
from app.repositories.preprocessing import PreprocessingRepository
from app.schemas.preprocessing import (
    PreprocessingRecommendationResponse,
    PreprocessingRunCreateRequest,
    PreprocessingRunResponse,
)
from app.services.preprocessing import PreprocessingService

router = APIRouter(prefix="/workspaces/{workspace_id}/datasets")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
PreprocessingManager = Annotated[
    User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))
]


async def load_dataset(session: AsyncSession, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID):
    dataset = await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id)
    if not dataset or dataset.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    return dataset


@router.get("/{dataset_id}/preprocessing/recommendations", response_model=list[PreprocessingRecommendationResponse])
async def get_recommendations(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    version_id: uuid.UUID | None = None,
) -> list[PreprocessingRecommendationResponse]:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    version = await DatasetRepository(session).get_version(dataset, version_id)
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset version not found")
    if version.status != "ready":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dataset version is not ready")
    return await PreprocessingService(session, get_settings()).recommendations(version)


@router.post("/{dataset_id}/preprocessing/runs", response_model=PreprocessingRunResponse)
async def execute_preprocessing(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: PreprocessingRunCreateRequest,
    session: Session,
    user: PreprocessingManager,
) -> PreprocessingRunResponse:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    run = await PreprocessingService(session, get_settings()).execute(user, dataset, request)
    return run


@router.get("/{dataset_id}/preprocessing/runs", response_model=list[PreprocessingRunResponse])
async def list_preprocessing_runs(
    workspace_id: uuid.UUID, dataset_id: uuid.UUID, session: Session, user: CurrentUser
) -> list[PreprocessingRunResponse]:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    return await PreprocessingRepository(session).list(dataset.id, user.id)


@router.get("/{dataset_id}/preprocessing/runs/{run_id}", response_model=PreprocessingRunResponse)
async def get_preprocessing_run(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    run_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
) -> PreprocessingRunResponse:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    run = await PreprocessingRepository(session).get(run_id, dataset.id, user.id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preprocessing run not found")
    return run


@router.post("/{dataset_id}/preprocessing/runs/{run_id}/undo", response_model=PreprocessingRunResponse)
async def undo_preprocessing(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    run_id: uuid.UUID,
    session: Session,
    user: PreprocessingManager,
) -> PreprocessingRunResponse:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    run = await PreprocessingRepository(session).get(run_id, dataset.id, user.id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preprocessing run not found")
    try:
        return await PreprocessingService(session, get_settings()).undo(run)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
