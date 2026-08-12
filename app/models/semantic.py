import uuid
from enum import StrEnum

from sqlalchemy import JSON, Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class SemanticStatus(StrEnum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class SemanticFieldRole(StrEnum):
    ENTITY = "entity"
    MEASURE = "measure"
    DIMENSION = "dimension"
    DATE = "date"
    KPI = "kpi"
    ATTRIBUTE = "attribute"


class SemanticRelationshipType(StrEnum):
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    RELATED = "related"


class SemanticLayer(TimestampMixin, Base):
    __tablename__ = "semantic_layers"
    __table_args__ = (UniqueConstraint("dataset_version_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"))
    dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dataset_versions.id", ondelete="CASCADE")
    )
    status: Mapped[str] = mapped_column(String(20), default=SemanticStatus.PROCESSING)
    business_domain: Mapped[str | None] = mapped_column(String(80))
    glossary_json: Mapped[dict | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)


class SemanticField(TimestampMixin, Base):
    __tablename__ = "semantic_fields"
    __table_args__ = (UniqueConstraint("semantic_layer_id", "source_column"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    semantic_layer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("semantic_layers.id", ondelete="CASCADE"))
    source_column: Mapped[str] = mapped_column(String(255))
    canonical_name: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(30))
    data_type: Mapped[str] = mapped_column(String(80))
    description: Mapped[str | None] = mapped_column(Text)
    expression: Mapped[str | None] = mapped_column(Text)
    synonyms: Mapped[list[str] | None] = mapped_column(JSON)
    confidence: Mapped[float] = mapped_column()
    is_user_defined: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")


class SemanticRelationship(TimestampMixin, Base):
    __tablename__ = "semantic_relationships"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    semantic_layer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("semantic_layers.id", ondelete="CASCADE"))
    source_field_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("semantic_fields.id", ondelete="CASCADE"))
    target_field_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("semantic_fields.id", ondelete="SET NULL"))
    relationship_type: Mapped[str] = mapped_column(String(30))
    confidence: Mapped[float] = mapped_column()
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, server_default="{}")


class GlossaryTerm(TimestampMixin, Base):
    __tablename__ = "glossary_terms"
    __table_args__ = (UniqueConstraint("workspace_id", "term"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"))
    term: Mapped[str] = mapped_column(String(255))
    definition: Mapped[str] = mapped_column(Text)
    synonyms: Mapped[list[str] | None] = mapped_column(JSON)
    example_values: Mapped[list[str] | None] = mapped_column(JSON)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
