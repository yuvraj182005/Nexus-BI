import uuid
from enum import StrEnum

from sqlalchemy import JSON, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class ProfileStatus(StrEnum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class DatasetProfileReport(TimestampMixin, Base):
    __tablename__ = "dataset_profile_reports"
    __table_args__ = (UniqueConstraint("dataset_version_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"))
    dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dataset_versions.id", ondelete="CASCADE")
    )
    status: Mapped[str] = mapped_column(String(20), default=ProfileStatus.PROCESSING)
    rows: Mapped[int | None] = mapped_column()
    columns: Mapped[int | None] = mapped_column()
    missing_values: Mapped[int | None] = mapped_column()
    duplicate_rows: Mapped[int | None] = mapped_column()
    duplicate_columns: Mapped[int | None] = mapped_column()
    quality_score: Mapped[float | None] = mapped_column()
    completeness_score: Mapped[float | None] = mapped_column()
    consistency_score: Mapped[float | None] = mapped_column()
    validity_score: Mapped[float | None] = mapped_column()
    uniqueness_score: Mapped[float | None] = mapped_column()
    overall_health_score: Mapped[float | None] = mapped_column()
    column_profiles: Mapped[list[dict] | None] = mapped_column(JSON)
    correlations: Mapped[dict | None] = mapped_column(JSON)
    relationships: Mapped[list[dict] | None] = mapped_column(JSON)
    data_distribution: Mapped[dict | None] = mapped_column(JSON)
    report_json: Mapped[dict | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
