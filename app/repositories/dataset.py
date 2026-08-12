import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.dataset import Dataset, DatasetLineage, DatasetPermission, DatasetVersion
from app.models.identity import User, UserRole


class DatasetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def scoped(self, user_organization_id: uuid.UUID, workspace_id: uuid.UUID):
        return select(Dataset).where(
            Dataset.organization_id == user_organization_id,
            Dataset.workspace_id == workspace_id,
        )

    async def get(self, dataset_id: uuid.UUID, organization_id: uuid.UUID, workspace_id: uuid.UUID) -> Dataset | None:
        statement = (
            self.scoped(organization_id, workspace_id)
            .where(Dataset.id == dataset_id)
            .options(selectinload(Dataset.tags), selectinload(Dataset.versions))
        )
        return await self.session.scalar(statement)

    async def get_for_user(self, dataset_id: uuid.UUID, user: User, workspace_id: uuid.UUID) -> Dataset | None:
        statement = self.scoped(user.organization_id, workspace_id).where(Dataset.id == dataset_id)
        if user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            statement = statement.where(
                or_(
                    Dataset.owner_id == user.id,
                    Dataset.permissions.any(DatasetPermission.user_id == user.id),
                )
            )
        statement = statement.options(selectinload(Dataset.tags), selectinload(Dataset.versions))
        return await self.session.scalar(statement)

    async def list(
        self, organization_id: uuid.UUID, workspace_id: uuid.UUID, include_deleted: bool = False
    ) -> list[Dataset]:
        statement = (
            self.scoped(organization_id, workspace_id)
            .options(selectinload(Dataset.tags), selectinload(Dataset.versions))
            .order_by(Dataset.created_at.desc())
        )
        if not include_deleted:
            statement = statement.where(Dataset.deleted_at.is_(None))
        return list((await self.session.scalars(statement)).all())

    async def list_for_user(self, user: User, workspace_id: uuid.UUID) -> list[Dataset]:
        statement = self.scoped(user.organization_id, workspace_id)
        if user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            statement = statement.where(
                or_(
                    Dataset.owner_id == user.id,
                    Dataset.permissions.any(DatasetPermission.user_id == user.id),
                )
            )
        statement = (
            statement.where(Dataset.deleted_at.is_(None))
            .options(selectinload(Dataset.tags), selectinload(Dataset.versions))
            .order_by(Dataset.created_at.desc())
        )
        return list((await self.session.scalars(statement)).all())

    async def next_version_number(self, dataset_id: uuid.UUID) -> int:
        value = await self.session.scalar(
            select(func.coalesce(func.max(DatasetVersion.version_number), 0)).where(
                DatasetVersion.dataset_id == dataset_id
            )
        )
        return int(value or 0) + 1

    async def get_version(self, dataset: Dataset, version_id: uuid.UUID | None) -> DatasetVersion | None:
        statement = select(DatasetVersion).where(DatasetVersion.dataset_id == dataset.id)
        if version_id:
            statement = statement.where(DatasetVersion.id == version_id)
        else:
            statement = statement.order_by(DatasetVersion.version_number.desc())
        return await self.session.scalar(statement)

    async def lineage(self, dataset_id: uuid.UUID) -> list[DatasetLineage]:
        statement = select(DatasetLineage).where(DatasetLineage.dataset_id == dataset_id)
        return list((await self.session.scalars(statement)).all())
