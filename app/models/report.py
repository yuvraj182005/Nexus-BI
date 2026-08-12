import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class GeneratedReportModel(TimestampMixin, Base):
    __tablename__ = "generated_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"))
    report_type: Mapped[str] = mapped_column(String(50))  # executive, business, analytics, data_quality
    title: Mapped[str] = mapped_column(String(255))
    format: Mapped[str] = mapped_column(String(20), default="markdown")
    content_payload: Mapped[dict] = mapped_column(JSON)
