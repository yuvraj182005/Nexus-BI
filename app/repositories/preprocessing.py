import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.preprocessing import PreprocessingRun


class PreprocessingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, run_id: uuid.UUID, dataset_id: uuid.UUID, user_id: uuid.UUID) -> PreprocessingRun | None:
        statement = (
            select(PreprocessingRun)
            .where(
                PreprocessingRun.id == run_id,
                PreprocessingRun.dataset_id == dataset_id,
                PreprocessingRun.initiated_by == user_id,
            )
            .options(selectinload(PreprocessingRun.steps))
        )
        return await self.session.scalar(statement)

    async def list(self, dataset_id: uuid.UUID, user_id: uuid.UUID) -> list[PreprocessingRun]:
        statement = (
            select(PreprocessingRun)
            .where(
                PreprocessingRun.dataset_id == dataset_id,
                PreprocessingRun.initiated_by == user_id,
            )
            .options(selectinload(PreprocessingRun.steps))
            .order_by(PreprocessingRun.created_at.desc())
        )
        return list((await self.session.scalars(statement)).all())
