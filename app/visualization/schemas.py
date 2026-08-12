from typing import Any

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    max_charts: int = Field(5, ge=1, le=20)


class ChartRecommendation(BaseModel):
    title: str
    chart_type: str  # bar, line, pie, scatter, heatmap, treemap, table, kpi_card
    x_axis: str | None
    y_axis: str | None
    reason: str


class RecommendationResponse(BaseModel):
    recommended_widgets: list[ChartRecommendation]
    suggested_layout: dict[str, Any]
    filters: list[str]


class ChartGenerateRequest(BaseModel):
    chart_type: str = Field("bar", description="bar, line, pie, scatter, heatmap, treemap, table, kpi_card")
    x_column: str | None = None
    y_column: str | None = None
    library: str = Field("plotly", description="plotly or echarts")


class ChartGenerateResponse(BaseModel):
    chart_type: str
    library: str
    spec_json: dict[str, Any]
    theme: str
