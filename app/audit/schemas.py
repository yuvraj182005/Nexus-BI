import uuid
from typing import Any

from pydantic import BaseModel, Field


class AuditLogRecord(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: float
    user_id: uuid.UUID
    workspace_id: uuid.UUID
    client_ip: str
    action: str  # login, logout, dataset_upload, dataset_delete, sql_execution, forecast, dashboard, insight, report, notification, workflow
    target: str
    status: str  # success, failure
    duration_ms: float
    details: dict[str, Any] = Field(default_factory=dict)


class AuditSearchRequest(BaseModel):
    user_id: uuid.UUID | None = None
    actions: list[str] | None = None
    status_filter: str | None = None
    start_time: float | None = None
    end_time: float | None = None
    limit: int = Field(50, ge=1, le=500)


class AuditSearchResponse(BaseModel):
    total_count: int
    logs: list[AuditLogRecord]


class AuditExportResponse(BaseModel):
    export_format: str
    export_url: str
    record_count: int
    data: str | list[dict[str, Any]]
