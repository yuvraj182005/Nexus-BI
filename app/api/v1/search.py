import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db_session
from app.models.identity import User
from app.search.schemas import GlobalSearchRequest, GlobalSearchResponse, SavedSearchCreateRequest
from app.search.service import global_search_service

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/search", response_model=GlobalSearchResponse)
async def global_enterprise_search(
    workspace_id: uuid.UUID,
    request: GlobalSearchRequest,
    session: Session,
    user: CurrentUser,
) -> GlobalSearchResponse:
    return global_search_service.search(request)


@router.post("/search/saved")
async def save_search_query(
    workspace_id: uuid.UUID,
    request: SavedSearchCreateRequest,
    session: Session,
    user: CurrentUser,
) -> dict[str, Any]:
    return global_search_service.save_search(request)


@router.get("/search/history")
async def get_search_history(
    workspace_id: uuid.UUID,
    user: CurrentUser,
) -> list[str]:
    return global_search_service.get_search_history()
