import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.dataset import DatasetPermission, DatasetStatus, DatasetTag, DatasetVersionStatus
from app.models.identity import User, UserRole
from app.repositories.dataset import DatasetRepository
from app.schemas.dataset import (
    DatasetDetailResponse,
    DatasetLineageResponse,
    DatasetPermissionRequest,
    DatasetPermissionResponse,
    DatasetPreviewResponse,
    DatasetResponse,
    DatasetUpdateRequest,
    DatasetVersionResponse,
)
from app.services.dataset import DatasetService
from app.tasks.dataset import process_dataset_version

router = APIRouter(prefix="/workspaces/{workspace_id}/datasets")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
DatasetManager = Annotated[
    User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))
]


def get_dataset_or_404(dataset, dataset_id: uuid.UUID):
    if not dataset or dataset.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} not found")
    return dataset


@router.post("", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    workspace_id: uuid.UUID,
    session: Session,
    user: DatasetManager,
    upload: Annotated[UploadFile, File(...)],
    name: Annotated[str, Form(min_length=2, max_length=255)],
    description: Annotated[str | None, Form(max_length=2000)] = None,
    tags: Annotated[str | None, Form(description="Comma-separated tags")] = None,
) -> DatasetResponse:
    try:
        dataset, version, process_async = await DatasetService(session, get_settings()).upload(
            user, workspace_id, upload, name, description, (tags or "").split(",")
        )
    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if process_async:
        process_dataset_version.delay(str(version.id))
    else:
        await DatasetService(session, get_settings()).process_version(version.id)
    refreshed = await DatasetRepository(session).get_for_user(dataset.id, user, workspace_id)
    return refreshed or dataset


@router.get("", response_model=list[DatasetResponse])
async def list_datasets(workspace_id: uuid.UUID, session: Session, user: CurrentUser) -> list[DatasetResponse]:
    return await DatasetRepository(session).list_for_user(user, workspace_id)


@router.get("/{dataset_id}", response_model=DatasetDetailResponse)
async def dataset_details(
    workspace_id: uuid.UUID, dataset_id: uuid.UUID, session: Session, user: CurrentUser
) -> DatasetDetailResponse:
    dataset = get_dataset_or_404(
        await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id), dataset_id
    )
    return dataset


@router.patch("/{dataset_id}", response_model=DatasetDetailResponse)
async def update_dataset(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    request: DatasetUpdateRequest,
    session: Session,
    user: DatasetManager,
) -> DatasetDetailResponse:
    repository = DatasetRepository(session)
    dataset = get_dataset_or_404(await repository.get_for_user(dataset_id, user, workspace_id), dataset_id)
    if request.name is not None:
        dataset.name = request.name
    if request.description is not None:
        dataset.description = request.description
    if request.tags is not None:
        dataset.tags.clear()
        dataset.tags.extend(
            DatasetTag(tag=tag.strip().lower()) for tag in sorted(set(request.tags)) if tag.strip()
        )
    await session.commit()
    return dataset


@router.delete("/{dataset_id}", response_model=DatasetResponse)
async def delete_dataset(
    workspace_id: uuid.UUID, dataset_id: uuid.UUID, session: Session, user: DatasetManager
) -> DatasetResponse:
    dataset = get_dataset_or_404(
        await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id), dataset_id
    )
    dataset.deleted_at = datetime.now(UTC)
    dataset.status = DatasetStatus.DELETED
    await session.commit()
    return dataset


@router.post("/{dataset_id}/restore", response_model=DatasetResponse)
async def restore_dataset(
    workspace_id: uuid.UUID, dataset_id: uuid.UUID, session: Session, user: DatasetManager
) -> DatasetResponse:
    dataset = await DatasetRepository(session).get(dataset_id, user.organization_id, workspace_id)
    if not dataset or dataset.deleted_at is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} not found")
    dataset.deleted_at = None
    dataset.status = DatasetStatus.READY if dataset.current_version_id else DatasetStatus.PROCESSING
    await session.commit()
    return dataset


@router.get("/{dataset_id}/versions", response_model=list[DatasetVersionResponse])
async def dataset_versions(
    workspace_id: uuid.UUID, dataset_id: uuid.UUID, session: Session, user: CurrentUser
) -> list[DatasetVersionResponse]:
    dataset = get_dataset_or_404(
        await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id), dataset_id
    )
    return list(dataset.versions)


@router.post("/{dataset_id}/versions", response_model=DatasetVersionResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset_version(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: DatasetManager,
    upload: Annotated[UploadFile, File(...)],
) -> DatasetVersionResponse:
    repository = DatasetRepository(session)
    dataset = get_dataset_or_404(await repository.get_for_user(dataset_id, user, workspace_id), dataset_id)
    try:
        version, process_async = await DatasetService(session, get_settings()).upload_version(dataset, upload)
    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if process_async:
        process_dataset_version.delay(str(version.id))
    else:
        await DatasetService(session, get_settings()).process_version(version.id)
    return await session.get(type(version), version.id) or version


@router.get("/{dataset_id}/preview", response_model=DatasetPreviewResponse)
async def preview_dataset(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    version_id: uuid.UUID | None = None,
) -> DatasetPreviewResponse:
    repository = DatasetRepository(session)
    dataset = get_dataset_or_404(await repository.get_for_user(dataset_id, user, workspace_id), dataset_id)
    version = await repository.get_version(dataset, version_id)
    if not version or version.status != DatasetVersionStatus.READY:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dataset version is not ready")
    try:
        columns, rows, truncated = await DatasetService(session, get_settings()).preview(version)
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return DatasetPreviewResponse(
        dataset_id=dataset.id, version_id=version.id, columns=columns, rows=rows, truncated=truncated
    )


@router.get("/{dataset_id}/lineage", response_model=list[DatasetLineageResponse])
async def dataset_lineage(
    workspace_id: uuid.UUID, dataset_id: uuid.UUID, session: Session, user: CurrentUser
) -> list[DatasetLineageResponse]:
    dataset = get_dataset_or_404(
        await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id), dataset_id
    )
    return await DatasetRepository(session).lineage(dataset.id)


@router.get("/{dataset_id}/permissions", response_model=list[DatasetPermissionResponse])
async def dataset_permissions(
    workspace_id: uuid.UUID, dataset_id: uuid.UUID, session: Session, user: CurrentUser
) -> list[DatasetPermissionResponse]:
    dataset = get_dataset_or_404(
        await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id), dataset_id
    )
    statement = select(DatasetPermission).where(DatasetPermission.dataset_id == dataset.id)
    return list((await session.scalars(statement)).all())


@router.put("/{dataset_id}/permissions/{target_user_id}", response_model=DatasetPermissionResponse)
async def set_dataset_permission(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    target_user_id: uuid.UUID,
    request: DatasetPermissionRequest,
    session: Session,
    user: DatasetManager,
) -> DatasetPermissionResponse:
    dataset = get_dataset_or_404(
        await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id), dataset_id
    )
    target_user = await session.scalar(
        select(User).where(User.id == target_user_id, User.organization_id == user.organization_id)
    )
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target user not found")
    permission = await session.scalar(
        select(DatasetPermission).where(
            DatasetPermission.dataset_id == dataset.id, DatasetPermission.user_id == target_user_id
        )
    )
    if permission is None:
        permission = DatasetPermission(dataset_id=dataset.id, user_id=target_user_id)
        session.add(permission)
    permission.permission = request.permission
    await session.commit()
    return permission
