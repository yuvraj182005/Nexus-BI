import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.dataset import DatasetStatus, DatasetVersionStatus


class DatasetUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    tags: list[str] | None = Field(default=None, max_length=30)


class DatasetTagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tag: str


class DatasetVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    version_number: int
    status: DatasetVersionStatus
    original_filename: str
    format: str
    content_type: str | None
    checksum_sha256: str
    file_size_bytes: int
    row_count: int | None
    column_count: int | None
    schema_json: list[dict] | None
    statistics_json: dict | None
    validation_json: dict | None
    error_message: str | None
    created_at: datetime


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    workspace_id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    slug: str
    description: str | None
    status: DatasetStatus
    current_version_id: uuid.UUID | None
    metadata_json: dict
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class DatasetDetailResponse(DatasetResponse):
    tags: list[DatasetTagResponse]


class DatasetPreviewResponse(BaseModel):
    dataset_id: uuid.UUID
    version_id: uuid.UUID
    columns: list[str]
    rows: list[dict]
    truncated: bool


class DatasetLineageResponse(BaseModel):
    id: uuid.UUID
    dataset_id: uuid.UUID
    source_dataset_id: uuid.UUID
    transformation: str
    metadata_json: dict


class DatasetPermissionRequest(BaseModel):
    permission: str = Field(pattern=r"^(view|edit|manage)$")


class DatasetPermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    permission: str
