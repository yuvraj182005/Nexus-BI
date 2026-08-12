import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self.session.scalar(select(User).where(User.id == user_id))

    async def get_by_email(self, organization_id: uuid.UUID, email: str) -> User | None:
        statement = select(User).where(User.organization_id == organization_id, User.email == email)
        return await self.session.scalar(statement)

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user
