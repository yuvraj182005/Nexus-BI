import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.preprocessing import (
    PreprocessingOperation,
    PreprocessingRunStatus,
    PreprocessingStepDecision,
)


class PreprocessingRecommendationResponse(BaseModel):
    id: uuid.UUID | None = None
    operation: PreprocessingOperation
    column_name: str | None
    parameters: dict
    reason: str
    confidence: float = Field(ge=0, le=1)
    impact: str
    estimated_improvement: float = Field(ge=0, le=100)


class PreprocessingStepRequest(BaseModel):
    operation: PreprocessingOperation
    column_name: str | None = None
    decision: PreprocessingStepDecision = PreprocessingStepDecision.ACCEPTED
    parameters: dict = Field(default_factory=dict)


class PreprocessingRunCreateRequest(BaseModel):
    source_version_id: uuid.UUID | None = None
    steps: list[PreprocessingStepRequest] = Field(min_length=1, max_length=50)


class PreprocessingStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    step_order: int
    operation: PreprocessingOperation
    column_name: str | None
    decision: PreprocessingStepDecision
    parameters: dict
    reason: str
    confidence: float
    impact: str
    estimated_improvement: float
    before_snapshot: dict | None
    after_snapshot: dict | None
    error_message: str | None


class PreprocessingRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    dataset_id: uuid.UUID
    source_version_id: uuid.UUID
    output_version_id: uuid.UUID | None
    initiated_by: uuid.UUID
    status: PreprocessingRunStatus
    quality_before: float | None
    quality_after: float | None
    undone_at: datetime | None
    error_message: str | None
    created_at: datetime
    steps: list[PreprocessingStepResponse] = Field(default_factory=list)
