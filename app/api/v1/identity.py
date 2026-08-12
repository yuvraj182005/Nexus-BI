import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_roles
from app.database.session import get_db_session
from app.identity.mfa import MFAService
from app.identity.providers import EnterpriseSSOProvider
from app.identity.schemas import (
    LoginHistoryRecord,
    MFASetupResponse,
    MFAVerifyRequest,
    PersonalAccessTokenRequest,
    PersonalAccessTokenResponse,
    ServiceAccountCreateRequest,
    ServiceAccountResponse,
    SSOLoginRequest,
    UserSessionResponse,
)
from app.identity.service import global_identity_service
from app.models.identity import User, UserRole

router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
IdentityAdmin = Annotated[User, Depends(require_roles(UserRole.ADMIN))]


@router.post("/auth/sso/login")
async def sso_login(request: SSOLoginRequest) -> dict:
    auth_data = await EnterpriseSSOProvider.authenticate_oauth2(request.provider, request.auth_code_or_token)
    return {"status": "authenticated", "user": auth_data}


@router.post("/auth/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(user: CurrentUser) -> MFASetupResponse:
    return MFAService.setup_mfa(user.email)


@router.post("/auth/mfa/verify")
async def verify_mfa(request: MFAVerifyRequest, user: CurrentUser) -> dict:
    valid = MFAService.verify_mfa(request.code, "secret")
    if not valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid MFA Code")
    return {"status": "verified"}


@router.post("/workspaces/{workspace_id}/identity/service-accounts", response_model=ServiceAccountResponse)
async def create_service_account(
    workspace_id: uuid.UUID,
    request: ServiceAccountCreateRequest,
    user: IdentityAdmin,
) -> ServiceAccountResponse:
    return await global_identity_service.create_service_account(workspace_id, request)


@router.post("/identity/tokens", response_model=PersonalAccessTokenResponse)
async def create_personal_access_token(
    request: PersonalAccessTokenRequest,
    user: CurrentUser,
) -> PersonalAccessTokenResponse:
    return await global_identity_service.create_personal_access_token(user.id, request)


@router.get("/identity/sessions", response_model=list[UserSessionResponse])
async def list_user_sessions(user: CurrentUser) -> list[UserSessionResponse]:
    return global_identity_service.get_user_sessions(user.id)


@router.get("/identity/login-history", response_model=list[LoginHistoryRecord])
async def list_login_history(user: IdentityAdmin) -> list[LoginHistoryRecord]:
    return global_identity_service.get_login_history()
