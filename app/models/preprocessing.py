import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


class PreprocessingRunStatus(StrEnum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    UNDONE = "undone"


class PreprocessingStepDecision(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CUSTOMIZED = "customized"
    APPLIED = "applied"
    FAILED = "failed"


class PreprocessingOperation(StrEnum):
    DROP_DUPLICATES = "drop_duplicates"
    IMPUTE_MISSING = "impute_missing"
    CLIP_OUTLIERS = "clip_outliers"
    PARSE_DATES = "parse_dates"
    STANDARDIZE_COLUMNS = "standardize_columns"
    ENCODE_CATEGORICAL = "encode_categorical"
    NORMALIZE_NUMERIC = "normalize_numeric"
    DERIVE_RATIO = "derive_ratio"
    VALIDATE_NOT_NULL = "validate_not_null"
    VALIDATE_RANGE = "validate_range"


class PreprocessingRun(TimestampMixin, Base):
    __tablename__ = "preprocessing_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"))
    source_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dataset_versions.id", ondelete="RESTRICT"))
    output_version_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("dataset_versions.id", ondelete="SET NULL")
    )
    initiated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    status: Mapped[str] = mapped_column(String(20), default=PreprocessingRunStatus.PROCESSING)
    quality_before: Mapped[float | None] = mapped_column()
    quality_after: Mapped[float | None] = mapped_column()
    undone_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)
    steps: Mapped[list["PreprocessingStep"]] = relationship(
        back_populates="run", cascade="all, delete-orphan", order_by="PreprocessingStep.step_order"
    )


class PreprocessingStep(TimestampMixin, Base):
    __tablename__ = "preprocessing_steps"
    __table_args__ = (UniqueConstraint("run_id", "step_order"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("preprocessing_runs.id", ondelete="CASCADE"))
    step_order: Mapped[int]
    operation: Mapped[str] = mapped_column(String(40))
    column_name: Mapped[str | None] = mapped_column(String(255))
    decision: Mapped[str] = mapped_column(String(20), default=PreprocessingStepDecision.PENDING)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict, server_default="{}")
    reason: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column()
    impact: Mapped[str] = mapped_column(String(20))
    estimated_improvement: Mapped[float] = mapped_column()
    before_snapshot: Mapped[dict | None] = mapped_column(JSON)
    after_snapshot: Mapped[dict | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
    run: Mapped[PreprocessingRun] = relationship(back_populates="steps")
