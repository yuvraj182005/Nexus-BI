import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User, UserRole
from app.repositories.dataset import DatasetRepository
from app.repositories.semantic import SemanticRepository
from app.schemas.semantic import (
    GlossaryTermCreateRequest,
    GlossaryTermResponse,
    SemanticFieldResponse,
    SemanticFieldUpdateRequest,
    SemanticLayerResponse,
)
from app.services.semantic import SemanticService

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
SemanticManager = Annotated[
    User, Depends(require_roles(UserRole.ADMIN, UserRole.ANALYST, UserRole.MANAGER))
]


async def load_dataset(session: AsyncSession, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID):
    dataset = await DatasetRepository(session).get_for_user(dataset_id, user, workspace_id)
    if not dataset or dataset.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    return dataset


async def load_layer(session: AsyncSession, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID, version_id: uuid.UUID | None):
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    layer = await SemanticRepository(session).get_layer(dataset.id, version_id)
    if not layer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Semantic layer not found")
    return dataset, layer


@router.get("/datasets/{dataset_id}/semantic", response_model=SemanticLayerResponse)
async def get_semantic_layer(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    version_id: uuid.UUID | None = None,
) -> SemanticLayerResponse:
    _, layer = await load_layer(session, user, workspace_id, dataset_id, version_id)
    fields = await SemanticRepository(session).get_fields(layer.id)
    relationships = await SemanticRepository(session).get_relationships(layer.id)
    return SemanticLayerResponse(
        id=layer.id,
        dataset_id=layer.dataset_id,
        dataset_version_id=layer.dataset_version_id,
        status=layer.status,
        business_domain=layer.business_domain,
        glossary_json=layer.glossary_json,
        error_message=layer.error_message,
        created_at=layer.created_at,
        updated_at=layer.updated_at,
        fields=fields,
        relationships=relationships,
    )


@router.post("/datasets/{dataset_id}/semantic", response_model=SemanticLayerResponse)
async def regenerate_semantic_layer(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    session: Session,
    user: SemanticManager,
    version_id: uuid.UUID | None = None,
) -> SemanticLayerResponse:
    dataset = await load_dataset(session, user, workspace_id, dataset_id)
    version = await DatasetRepository(session).get_version(dataset, version_id)
    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset version not found")
    layer = await SemanticService(session, get_settings()).generate(version.id)
    if not layer:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profiling report is not ready")
    fields = await SemanticRepository(session).get_fields(layer.id)
    relationships = await SemanticRepository(session).get_relationships(layer.id)
    return SemanticLayerResponse(
        id=layer.id, dataset_id=layer.dataset_id, dataset_version_id=layer.dataset_version_id,
        status=layer.status, business_domain=layer.business_domain, glossary_json=layer.glossary_json,
        error_message=layer.error_message, created_at=layer.created_at, updated_at=layer.updated_at,
        fields=fields, relationships=relationships,
    )


@router.patch("/datasets/{dataset_id}/semantic/fields/{source_column}", response_model=SemanticFieldResponse)
async def update_semantic_field(
    workspace_id: uuid.UUID,
    dataset_id: uuid.UUID,
    source_column: str,
    request: SemanticFieldUpdateRequest,
    session: Session,
    user: SemanticManager,
    version_id: uuid.UUID | None = None,
) -> SemanticFieldResponse:
    _, layer = await load_layer(session, user, workspace_id, dataset_id, version_id)
    try:
        return await SemanticService(session, get_settings()).update_field(layer, source_column, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/glossary", response_model=list[GlossaryTermResponse])
async def list_glossary(workspace_id: uuid.UUID, session: Session, user: CurrentUser):
    return await SemanticRepository(session).list_glossary(workspace_id)


@router.post("/glossary", response_model=GlossaryTermResponse, status_code=status.HTTP_201_CREATED)
async def create_glossary(
    workspace_id: uuid.UUID,
    request: GlossaryTermCreateRequest,
    session: Session,
    user: SemanticManager,
) -> GlossaryTermResponse:
    try:
        return await SemanticService(session, get_settings()).create_glossary_term(user, workspace_id, request)
    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
