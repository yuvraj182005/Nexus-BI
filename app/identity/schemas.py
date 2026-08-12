import uuid

from pydantic import BaseModel, Field


class SSOLoginRequest(BaseModel):
    provider: str = Field(..., description="google, github, entra_id, ldap, oidc")
    auth_code_or_token: str
    redirect_uri: str | None = None


class MFASetupResponse(BaseModel):
    secret: str
    qr_code_uri: str
    backup_codes: list[str]


class MFAVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)


class ServiceAccountCreateRequest(BaseModel):
    name: str = Field(..., description="Service account descriptor name")
    role: str = Field("analyst", description="admin, analyst, manager, viewer")
    scopes: list[str] = Field(default_factory=lambda: ["read", "execute"])


class ServiceAccountResponse(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    name: str
    role: str
    client_id: str
    client_secret: str
    created_at: float


class PersonalAccessTokenRequest(BaseModel):
    name: str = Field(..., description="Token name, e.g. CLI Access")
    expires_in_days: int = Field(90, ge=1, le=365)


class PersonalAccessTokenResponse(BaseModel):
    token_id: str
    token_name: str
    raw_token: str
    expires_at: float


class UserSessionResponse(BaseModel):
    session_id: str
    user_id: uuid.UUID
    device_name: str
    ip_address: str
    is_trusted: bool
    last_active: float
    created_at: float


class LoginHistoryRecord(BaseModel):
    id: str
    timestamp: float
    ip_address: str
    user_agent: str
    auth_method: str
    status: str
