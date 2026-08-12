import uuid
from typing import Any

from pydantic import BaseModel, Field


class WorkflowStepConfig(BaseModel):
    step_id: str
    action: str  # upload, profile, clean, semantic, sql, analytics, forecast, insights, dashboard, report, notification, archive
    params: dict[str, Any] = Field(default_factory=dict)
    retry_count: int = Field(3, ge=0)


class WorkflowTemplate(BaseModel):
    template_id: str
    name: str
    description: str
    version: str = "1.0.0"
    steps: list[WorkflowStepConfig]


class WorkflowExecuteRequest(BaseModel):
    template_id: str = Field("end_to_end_analytics", description="Target workflow template ID")
    dataset_id: uuid.UUID | None = None
    custom_params: dict[str, Any] = Field(default_factory=dict)


class WorkflowExecutionResponse(BaseModel):
    execution_id: str
    template_id: str
    status: str  # queued, running, completed, failed
    total_steps: int
    completed_steps: int
    duration_ms: float
    step_results: list[dict[str, Any]]
    logs: list[str]
