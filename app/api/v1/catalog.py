import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.catalog.schemas import CatalogItem, CatalogSearchRequest, CatalogSearchResponse
from app.catalog.service import DataCatalogService
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/catalog/search", response_model=CatalogSearchResponse)
async def search_catalog(
    workspace_id: uuid.UUID,
    request: CatalogSearchRequest,
    session: Session,
    user: CurrentUser,
) -> CatalogSearchResponse:
    return await DataCatalogService(session, get_settings()).search(workspace_id, request)


@router.post("/catalog/{item_id}/star", response_model=CatalogItem)
async def toggle_star_catalog_item(
    workspace_id: uuid.UUID,
    item_id: str,
    session: Session,
    user: CurrentUser,
) -> CatalogItem:
    try:
        return await DataCatalogService(session, get_settings()).toggle_star(item_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
