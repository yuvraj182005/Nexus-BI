import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.connector import ConnectorStatus, ConnectorType, SyncStatus


class ConnectorCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    connector_type: ConnectorType
    config: dict = Field(default_factory=dict)
    credentials: dict = Field(default_factory=dict)
    sync_enabled: bool = False
    sync_interval_minutes: int | None = Field(default=None, ge=1, le=10080)


class ConnectorUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    config: dict | None = None
    credentials: dict | None = None
    sync_enabled: bool | None = None
    sync_interval_minutes: int | None = Field(default=None, ge=1, le=10080)


class ConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    workspace_id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    connector_type: ConnectorType
    status: ConnectorStatus
    config_json: dict
    sync_enabled: bool
    sync_interval_minutes: int | None
    last_health_check_at: datetime | None
    last_sync_at: datetime | None
    last_error: str | None
    created_at: datetime
    updated_at: datetime


class ConnectorColumnResponse(BaseModel):
    name: str
    data_type: str
    nullable: bool
    cardinality: int | None = None


class ConnectorTableResponse(BaseModel):
    name: str
    columns: list[ConnectorColumnResponse]
    row_count: int | None


class ConnectorDiscoveryResponse(BaseModel):
    connector_id: uuid.UUID
    tables: list[ConnectorTableResponse]


class ConnectorHealthResponse(BaseModel):
    connector_id: uuid.UUID
    status: ConnectorStatus
    healthy: bool
    message: str
    latency_ms: float | None


class ConnectorSyncResponse(BaseModel):
    connector_id: uuid.UUID
    run_id: uuid.UUID
    status: SyncStatus
    rows_synced: int | None
    tables: list[ConnectorTableResponse] = Field(default_factory=list)
    error_message: str | None
