import asyncio
import uuid

from app.database.session import session_factory
from app.services.dataset import DatasetService
from app.tasks.celery_app import celery_app


@celery_app.task(name="nexusbi.process_dataset_version", autoretry_for=(Exception,), retry_backoff=True)
def process_dataset_version(version_id: str) -> None:
    async def run() -> None:
        async with session_factory() as session:
            await DatasetService(session, __import__("app.core.config", fromlist=["get_settings"]).get_settings()).process_version(
                uuid.UUID(version_id)
            )

    asyncio.run(run())
