import time
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.identity.schemas import (
    LoginHistoryRecord,
    PersonalAccessTokenRequest,
    PersonalAccessTokenResponse,
    ServiceAccountCreateRequest,
    ServiceAccountResponse,
    UserSessionResponse,
)


class EnterpriseIdentityService:
    def __init__(self, session: AsyncSession | None = None, settings: Settings | None = None) -> None:
        self.session = session
        self.settings = settings
        self._sessions: dict[str, UserSessionResponse] = {}
        self._login_history: list[LoginHistoryRecord] = []

    async def create_service_account(self, workspace_id: uuid.UUID, request: ServiceAccountCreateRequest) -> ServiceAccountResponse:
        client_id = f"sa_{uuid.uuid4().hex[:12]}"
        client_secret = f"sec_{uuid.uuid4().hex}"
        return ServiceAccountResponse(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            name=request.name,
            role=request.role,
            client_id=client_id,
            client_secret=client_secret,
            created_at=time.time(),
        )

    async def create_personal_access_token(self, user_id: uuid.UUID, request: PersonalAccessTokenRequest) -> PersonalAccessTokenResponse:
        raw_token = f"pat_nexusbi_{uuid.uuid4().hex}"
        expires_at = time.time() + (request.expires_in_days * 86400)
        return PersonalAccessTokenResponse(
            token_id=uuid.uuid4().hex[:8],
            token_name=request.name,
            raw_token=raw_token,
            expires_at=expires_at,
        )

    def record_login(self, user_id: uuid.UUID, ip_address: str, user_agent: str, method: str) -> UserSessionResponse:
        session_id = f"sess_{uuid.uuid4().hex}"
        sess = UserSessionResponse(
            session_id=session_id,
            user_id=user_id,
            device_name=user_agent[:30] if user_agent else "Web Browser",
            ip_address=ip_address,
            is_trusted=True,
            last_active=time.time(),
            created_at=time.time(),
        )
        self._sessions[session_id] = sess

        hist = LoginHistoryRecord(
            id=uuid.uuid4().hex,
            timestamp=time.time(),
            ip_address=ip_address,
            user_agent=user_agent,
            auth_method=method,
            status="success",
        )
        self._login_history.append(hist)
        return sess

    def get_user_sessions(self, user_id: uuid.UUID) -> list[UserSessionResponse]:
        return [s for s in self._sessions.values() if s.user_id == user_id]

    def get_login_history(self) -> list[LoginHistoryRecord]:
        return list(self._login_history)


global_identity_service = EnterpriseIdentityService()
