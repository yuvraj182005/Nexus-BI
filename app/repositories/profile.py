import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import DatasetProfileReport


class ProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_for_dataset(
        self, dataset_id: uuid.UUID, version_id: uuid.UUID | None = None
    ) -> DatasetProfileReport | None:
        statement = select(DatasetProfileReport).where(DatasetProfileReport.dataset_id == dataset_id)
        if version_id:
            statement = statement.where(DatasetProfileReport.dataset_version_id == version_id)
        else:
            statement = statement.order_by(DatasetProfileReport.created_at.desc())
        return await self.session.scalar(statement)
