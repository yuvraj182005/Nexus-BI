import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.repositories.dataset import DatasetRepository
from app.repositories.profile import ProfileRepository
from app.schemas.profile import DatasetProfileResponse
from app.services.profiling import ProfilingService

router = APIRouter(prefix="/workspaces/{workspace_id}/datasets")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ProfileManager = Annotated[
    User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))
]


async def load_dataset(session: AsyncSession, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID):
    dataset = await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id)
    if not dataset or dataset.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    return dataset


@router.get("/{dataset_id}/profile", response_model=DatasetProfileResponse)
async def get_profile(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    version_id: uuid.UUID | None = None,
) -> DatasetProfileResponse:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    report = await ProfileRepository(session).get_for_dataset(dataset.id, version_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile report not found")
    return report


@router.get("/{dataset_id}/profile/download")
async def download_profile(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    version_id: uuid.UUID | None = None,
) -> JSONResponse:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    report = await ProfileRepository(session).get_for_dataset(dataset.id, version_id)
    if not report or not report.report_json:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile report not found")
    return JSONResponse(
        content=report.report_json,
        headers={"Content-Disposition": f'attachment; filename="{dataset.slug}-profile.json"'},
    )


@router.post("/{dataset_id}/profile", response_model=DatasetProfileResponse, status_code=status.HTTP_202_ACCEPTED)
async def regenerate_profile(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: ProfileManager,
    version_id: uuid.UUID | None = None,
) -> DatasetProfileResponse:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    version = await DatasetRepository(session).get_version(dataset, version_id)
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset version not found")
    report = await ProfilingService(session, get_settings()).generate(version.id)
    if not report:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dataset version is not ready")
    return report
