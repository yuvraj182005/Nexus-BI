import uuid

from sqlalchemy import JSON, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class BusinessInsightModel(TimestampMixin, Base):
    __tablename__ = "business_insights"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text)
    what_happened: Mapped[str] = mapped_column(Text)
    why_it_happened: Mapped[str] = mapped_column(Text)
    evidence: Mapped[dict | None] = mapped_column(JSON)
    affected_kpis: Mapped[list[str] | None] = mapped_column(JSON)
    business_impact: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(50), default="medium")
    risk: Mapped[str] = mapped_column(String(50), default="low")
    confidence: Mapped[float] = mapped_column(Float, default=0.9)
    recommendation: Mapped[str] = mapped_column(Text)
    expected_roi: Mapped[str | None] = mapped_column(String(100))
    next_action: Mapped[str | None] = mapped_column(Text)


class WhatIfScenarioModel(TimestampMixin, Base):
    __tablename__ = "what_if_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    parameters_json: Mapped[dict] = mapped_column(JSON)
    projected_kpis_json: Mapped[dict] = mapped_column(JSON)
