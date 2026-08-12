import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.semantic import SemanticFieldRole, SemanticRelationshipType, SemanticStatus


class SemanticFieldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_column: str
    canonical_name: str
    display_name: str
    role: SemanticFieldRole
    data_type: str
    description: str | None
    expression: str | None
    synonyms: list[str] | None
    confidence: float
    is_user_defined: bool


class SemanticRelationshipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_field_id: uuid.UUID
    target_field_id: uuid.UUID | None
    relationship_type: SemanticRelationshipType
    confidence: float
    metadata_json: dict


class SemanticLayerResponse(BaseModel):
    id: uuid.UUID
    dataset_id: uuid.UUID
    dataset_version_id: uuid.UUID
    status: SemanticStatus
    business_domain: str | None
    glossary_json: dict | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    fields: list[SemanticFieldResponse] = Field(default_factory=list)
    relationships: list[SemanticRelationshipResponse] = Field(default_factory=list)


class SemanticFieldUpdateRequest(BaseModel):
    canonical_name: str | None = Field(default=None, min_length=2, max_length=255)
    display_name: str | None = Field(default=None, min_length=2, max_length=255)
    role: SemanticFieldRole | None = None
    description: str | None = Field(default=None, max_length=2000)
    expression: str | None = Field(default=None, max_length=2000)
    synonyms: list[str] | None = Field(default=None, max_length=30)


class GlossaryTermCreateRequest(BaseModel):
    term: str = Field(min_length=2, max_length=255)
    definition: str = Field(min_length=2, max_length=2000)
    synonyms: list[str] = Field(default_factory=list, max_length=30)
    example_values: list[str] = Field(default_factory=list, max_length=30)


class GlossaryTermResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    workspace_id: uuid.UUID
    term: str
    definition: str
    synonyms: list[str] | None
    example_values: list[str] | None
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
