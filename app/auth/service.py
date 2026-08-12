from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.auth.security import TokenType, create_token, hash_password, verify_password
from app.models.identity import Organization, User, UserRole


class AuthService:
    def __init__(self, session: AsyncSession, access_minutes: int, refresh_days: int) -> None:
        self.session = session
        self.access_minutes = access_minutes
        self.refresh_days = refresh_days

    async def register(self, request: RegisterRequest) -> TokenResponse:
        existing = await self.session.scalar(
            select(Organization).where(Organization.slug == request.organization_slug)
        )
        if existing:
            raise ValueError("Organization slug is already registered")

        organization = Organization(name=request.organization_name, slug=request.organization_slug)
        self.session.add(organization)
        await self.session.flush()
        user = User(
            organization_id=organization.id,
            email=str(request.email).lower(),
            password_hash=hash_password(request.password),
            role=UserRole.ADMIN,
            is_verified=False,
        )
        self.session.add(user)
        await self.session.commit()
        return self._tokens(str(user.id))

    async def login(self, request: LoginRequest) -> TokenResponse:
        statement = (
            select(User)
            .join(Organization)
            .where(Organization.slug == request.organization_slug)
            .where(User.email == str(request.email).lower())
        )
        user = await self.session.scalar(statement)
        if not user or not user.is_active or not user.password_hash:
            raise ValueError("Invalid credentials")
        if not verify_password(request.password, user.password_hash):
            raise ValueError("Invalid credentials")
        return self._tokens(str(user.id))

    def _tokens(self, subject: str) -> TokenResponse:
        return TokenResponse(
            access_token=create_token(
                subject, TokenType.ACCESS, timedelta(minutes=self.access_minutes)
            ),
            refresh_token=create_token(
                subject, TokenType.REFRESH, timedelta(days=self.refresh_days)
            ),
        )
