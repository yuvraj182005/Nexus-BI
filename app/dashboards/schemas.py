import uuid
from typing import Any

from pydantic import BaseModel, Field


class DashboardGridWidget(BaseModel):
    widget_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    title: str
    chart_type: str  # bar, line, pie, scatter, kpi_card, table
    x: int = Field(0, ge=0)
    y: int = Field(0, ge=0)
    w: int = Field(6, ge=1, le=12)
    h: int = Field(4, ge=1)
    dataset_id: uuid.UUID | None = None
    query_sql: str | None = None
    plotly_config: dict[str, Any] = Field(default_factory=dict)
    cross_filters: list[str] = Field(default_factory=list)


class DashboardCreateRequest(BaseModel):
    title: str = Field(..., description="Dashboard name")
    description: str | None = None
    theme: str = Field("dark_glassmorphism", description="dark_glassmorphism, light_minimal, corporate_blue")
    template_id: str | None = None
    widgets: list[DashboardGridWidget] = Field(default_factory=list)
    global_filters: dict[str, Any] = Field(default_factory=dict)


class DashboardDetailResponse(BaseModel):
    id: str
    workspace_id: uuid.UUID
    title: str
    description: str | None
    theme: str
    version: int = 1
    widgets: list[DashboardGridWidget]
    global_filters: dict[str, Any]
    bookmarks: list[dict[str, Any]]
    is_public_shared: bool = False
    embed_url: str
    created_at: float


class DashboardSnapshotResponse(BaseModel):
    snapshot_id: str
    dashboard_id: str
    rendered_image_url: str
    pdf_export_url: str
    timestamp: float
