import uuid
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobCreateRequest(BaseModel):
    job_type: str = Field(..., description="dataset_upload, forecast, dashboard_generation, report_generation, chat_rag, insight_generation")
    parent_job_id: uuid.UUID | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class JobResponse(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    job_type: str
    status: JobStatus
    progress_percent: float
    retry_count: int
    parent_job_id: uuid.UUID | None
    child_job_ids: list[uuid.UUID]
    worker: str
    logs: list[str]
    error_message: str | None
    result_metadata: dict[str, Any] | None
    created_at: Any
    updated_at: Any


class JobDashboardSummary(BaseModel):
    total_jobs: int
    queued: int
    running: int
    completed: int
    failed: int
    cancelled: int
    recent_jobs: list[JobResponse]
