import asyncio
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.config import get_settings
from app.database.session import session_factory
from app.models.connector import ConnectorSyncRun, DataConnector
from app.services.connector import ConnectorService
from app.tasks.celery_app import celery_app


@celery_app.task(name="nexusbi.sync_connector", autoretry_for=(Exception,), retry_backoff=True)
def sync_connector(connector_id: str, run_id: str) -> None:
    async def run() -> None:
        async with session_factory() as session:
            connector = await session.get(DataConnector, uuid.UUID(connector_id))
            sync_run = await session.get(ConnectorSyncRun, uuid.UUID(run_id))
            if connector and sync_run:
                await ConnectorService(session, get_settings()).sync(connector, sync_run)

    asyncio.run(run())


@celery_app.task(name="nexusbi.dispatch_scheduled_connector_syncs")
def dispatch_scheduled_connector_syncs() -> None:
    async def run() -> None:
        async with session_factory() as session:
            connectors = list(
                (
                    await session.scalars(
                        select(DataConnector).where(
                            DataConnector.sync_enabled.is_(True),
                            DataConnector.status != "disabled",
                        )
                    )
                ).all()
            )
            now = datetime.now(UTC)
            pending_runs: list[tuple[uuid.UUID, uuid.UUID]] = []
            for connector in connectors:
                interval = connector.sync_interval_minutes or get_settings().connector_sync_interval_minutes
                if connector.last_sync_at is None or connector.last_sync_at <= now - timedelta(minutes=interval):
                    sync_run = ConnectorSyncRun(connector_id=connector.id)
                    session.add(sync_run)
                    await session.flush()
                    pending_runs.append((connector.id, sync_run.id))
            await session.commit()
            for connector_id, run_id in pending_runs:
                sync_connector.delay(str(connector_id), str(run_id))

    asyncio.run(run())