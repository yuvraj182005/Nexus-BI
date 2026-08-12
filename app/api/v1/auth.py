from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.schemas import CurrentUserResponse, LoginRequest, RegisterRequest, TokenResponse
from app.auth.service import AuthService
from app.core.config import get_settings
from app.database.session import get_db_session
from app.models.identity import User

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TokenResponse:
    try:
        settings = get_settings()
        return await AuthService(
            session, settings.access_token_expire_minutes, settings.refresh_token_expire_days
        ).register(request)
    except ValueError as exc:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TokenResponse:
    try:
        settings = get_settings()
        return await AuthService(
            session, settings.access_token_expire_minutes, settings.refresh_token_expire_days
        ).login(request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.get("/me", response_model=CurrentUserResponse)
async def me(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user
