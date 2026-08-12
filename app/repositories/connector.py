import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.connector import ConnectorSyncRun, DataConnector
from app.models.identity import User, UserRole


class ConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, connector_id: uuid.UUID, user: User, workspace_id: uuid.UUID) -> DataConnector | None:
        statement = select(DataConnector).where(
            DataConnector.id == connector_id,
            DataConnector.organization_id == user.organization_id,
            DataConnector.workspace_id == workspace_id,
        )
        if user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            statement = statement.where(DataConnector.owner_id == user.id)
        return await self.session.scalar(statement)

    async def list(self, user: User, workspace_id: uuid.UUID) -> list[DataConnector]:
        statement = select(DataConnector).where(
            DataConnector.organization_id == user.organization_id,
            DataConnector.workspace_id == workspace_id,
        )
        if user.role not in {UserRole.ADMIN, UserRole.MANAGER}:
            statement = statement.where(DataConnector.owner_id == user.id)
        return list((await self.session.scalars(statement.order_by(DataConnector.created_at.desc()))).all())

    async def add(self, connector: DataConnector) -> DataConnector:
        self.session.add(connector)
        await self.session.flush()
        return connector

    async def name_exists(self, workspace_id: uuid.UUID, name: str) -> bool:
        return bool(
            await self.session.scalar(
                select(DataConnector.id).where(
                    DataConnector.workspace_id == workspace_id, DataConnector.name == name
                )
            )
        )

    async def create_run(self, connector_id: uuid.UUID) -> ConnectorSyncRun:
        run = ConnectorSyncRun(connector_id=connector_id)
        self.session.add(run)
        await self.session.flush()
        return run
