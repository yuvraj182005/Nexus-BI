import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.connectors.base import ConnectorContext, ConnectorError
from app.connectors.registry import get_adapter
from app.connectors.security import decrypt_credentials, encrypt_credentials
from app.core.config import Settings
from app.models.connector import ConnectorStatus, ConnectorSyncRun, DataConnector, SyncStatus
from app.models.identity import User
from app.repositories.connector import ConnectorRepository
from app.schemas.connector import ConnectorCreateRequest, ConnectorUpdateRequest


class ConnectorService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.repository = ConnectorRepository(session)

    async def create(self, user: User, workspace_id: uuid.UUID, request: ConnectorCreateRequest) -> DataConnector:
        if await self.repository.name_exists(workspace_id, request.name):
            raise ValueError("Connector name already exists in this workspace")
        connector = DataConnector(
            organization_id=user.organization_id,
            workspace_id=workspace_id,
            owner_id=user.id,
            name=request.name,
            connector_type=request.connector_type.value,
            config_json=request.config,
            credentials_encrypted=encrypt_credentials(request.credentials),
            sync_enabled=request.sync_enabled,
            sync_interval_minutes=request.sync_interval_minutes or self.settings.connector_sync_interval_minutes,
        )
        await self.repository.add(connector)
        await self.session.commit()
        return connector

    async def update(self, connector: DataConnector, request: ConnectorUpdateRequest) -> DataConnector:
        if request.name is not None:
            connector.name = request.name
        if request.config is not None:
            connector.config_json = request.config
        if request.credentials is not None:
            connector.credentials_encrypted = encrypt_credentials(request.credentials)
        if request.sync_enabled is not None:
            connector.sync_enabled = request.sync_enabled
        if request.sync_interval_minutes is not None:
            connector.sync_interval_minutes = request.sync_interval_minutes
        await self.session.commit()
        return connector

    async def validate(self, connector: DataConnector) -> tuple[bool, str, float | None]:
        try:
            result = await get_adapter(connector.connector_type).validate(self._context(connector))
        except (ConnectorError, ValueError) as exc:
            connector.status = ConnectorStatus.UNHEALTHY
            connector.last_error = str(exc)
            connector.last_health_check_at = datetime.now(UTC)
            await self.session.commit()
            return False, str(exc), None
        connector.status = ConnectorStatus.HEALTHY
        connector.last_error = None
        connector.last_health_check_at = datetime.now(UTC)
        await self.session.commit()
        return result.healthy, result.message, result.latency_ms

    async def discover_schema(self, connector: DataConnector):
        try:
            return await get_adapter(connector.connector_type).discover_schema(self._context(connector))
        except (ConnectorError, ValueError) as exc:
            raise ConnectorError(str(exc)) from exc

    async def sync(self, connector: DataConnector, run: ConnectorSyncRun):
        try:
            rows, tables = await get_adapter(connector.connector_type).sync(self._context(connector))
            run.status = SyncStatus.SUCCEEDED
            run.rows_synced = rows
            run.schema_json = [
                {"name": table.name, "columns": [column.__dict__ for column in table.columns], "row_count": table.row_count}
                for table in tables
            ]
            connector.status = ConnectorStatus.HEALTHY
            connector.last_sync_at = datetime.now(UTC)
            connector.last_error = None
        except (ConnectorError, ValueError) as exc:
            run.status = SyncStatus.FAILED
            run.error_message = str(exc)
            connector.status = ConnectorStatus.UNHEALTHY
            connector.last_error = str(exc)
        await self.session.commit()
        return run

    def _context(self, connector: DataConnector) -> ConnectorContext:
        return ConnectorContext(connector.config_json or {}, decrypt_credentials(connector.credentials_encrypted))
