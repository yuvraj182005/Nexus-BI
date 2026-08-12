import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class ConnectorType(StrEnum):
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    PARQUET = "parquet"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQL_SERVER = "sql_server"
    SQLITE = "sqlite"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    MONGODB = "mongodb"
    GOOGLE_SHEETS = "google_sheets"
    REST_API = "rest_api"


class ConnectorStatus(StrEnum):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DISABLED = "disabled"


class SyncStatus(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class DataConnector(TimestampMixin, Base):
    __tablename__ = "data_connectors"
    __table_args__ = (UniqueConstraint("workspace_id", "name"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"))
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    name: Mapped[str] = mapped_column(String(255))
    connector_type: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default=ConnectorStatus.UNKNOWN)
    config_json: Mapped[dict] = mapped_column(JSON, default=dict, server_default="{}")
    credentials_encrypted: Mapped[str | None] = mapped_column(Text)
    sync_enabled: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    sync_interval_minutes: Mapped[int | None] = mapped_column(Integer)
    last_health_check_at: Mapped[datetime | None] = mapped_column()
    last_sync_at: Mapped[datetime | None] = mapped_column()
    last_error: Mapped[str | None] = mapped_column(Text)


class ConnectorSyncRun(TimestampMixin, Base):
    __tablename__ = "connector_sync_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    connector_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("data_connectors.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default=SyncStatus.RUNNING)
    rows_synced: Mapped[int | None] = mapped_column(BigInteger)
    schema_json: Mapped[list[dict] | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
