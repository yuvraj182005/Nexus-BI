import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.profile import ProfileStatus


class DatasetProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    dataset_id: uuid.UUID
    dataset_version_id: uuid.UUID
    status: ProfileStatus
    rows: int | None
    columns: int | None
    missing_values: int | None
    duplicate_rows: int | None
    duplicate_columns: int | None
    quality_score: float | None
    completeness_score: float | None
    consistency_score: float | None
    validity_score: float | None
    uniqueness_score: float | None
    overall_health_score: float | None
    column_profiles: list[dict] | None
    correlations: dict | None
    relationships: list[dict] | None
    data_distribution: dict | None
    report_json: dict | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime
