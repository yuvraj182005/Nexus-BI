import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db_session
from app.marketplace.schemas import MarketplaceItem, MarketplaceReviewRequest
from app.marketplace.service import global_marketplace_service
from app.models.identity import User

router = APIRouter(prefix="/workspaces/{workspace_id}")
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/marketplace/items", response_model=list[MarketplaceItem])
async def list_marketplace_items(
    workspace_id: uuid.UUID,
    session: Session,
    user: CurrentUser,
    item_type: str | None = None,
) -> list[MarketplaceItem]:
    return global_marketplace_service.list_items(item_type)


@router.post("/marketplace/items/{item_id}/install", response_model=MarketplaceItem)
async def install_marketplace_item(
    workspace_id: uuid.UUID,
    item_id: str,
    session: Session,
    user: CurrentUser,
) -> MarketplaceItem:
    try:
        return global_marketplace_service.install_item(item_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/marketplace/items/{item_id}/review", response_model=MarketplaceItem)
async def submit_marketplace_item_review(
    workspace_id: uuid.UUID,
    item_id: str,
    request: MarketplaceReviewRequest,
    session: Session,
    user: CurrentUser,
) -> MarketplaceItem:
    try:
        return global_marketplace_service.submit_review(item_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
