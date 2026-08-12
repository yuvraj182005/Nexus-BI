import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.observability import AIObservabilityLogger
from app.models.identity import User
from app.repositories.dataset import DatasetRepository
from app.repositories.semantic import SemanticRepository
from app.visualization.schemas import (
    ChartGenerateRequest,
    ChartGenerateResponse,
    ChartRecommendation,
    RecommendationRequest,
    RecommendationResponse,
)


class VisualizationService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.dataset_repo = DatasetRepository(session)
        self.semantic_repo = SemanticRepository(session)

    async def recommend(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID, request: RecommendationRequest) -> RecommendationResponse:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset:
            raise ValueError("Dataset not found")

        layer = await self.semantic_repo.get_layer(dataset.id)
        fields = await self.semantic_repo.get_fields(layer.id) if layer else []

        measures = [f for f in fields if f.role in ("measure", "kpi")]
        dimensions = [f for f in fields if f.role in ("dimension", "entity")]
        dates = [f for f in fields if f.role == "date"]

        widgets = []

        if dates and measures:
            widgets.append(
                ChartRecommendation(
                    title=f"{measures[0].display_name} Over Time",
                    chart_type="line",
                    x_axis=dates[0].source_column,
                    y_axis=measures[0].source_column,
                    reason="Ideal for analyzing temporal trends in key metrics.",
                )
            )

        if dimensions and measures:
            widgets.append(
                ChartRecommendation(
                    title=f"{measures[0].display_name} by {dimensions[0].display_name}",
                    chart_type="bar",
                    x_axis=dimensions[0].source_column,
                    y_axis=measures[0].source_column,
                    reason="Best for comparing values across categorical groupings.",
                )
            )

        if len(measures) >= 2:
            widgets.append(
                ChartRecommendation(
                    title=f"Correlation: {measures[0].display_name} vs {measures[1].display_name}",
                    chart_type="scatter",
                    x_axis=measures[0].source_column,
                    y_axis=measures[1].source_column,
                    reason="Helpful for discovering relationship patterns between two continuous variables.",
                )
            )

        if not widgets:
            widgets.append(
                ChartRecommendation(
                    title="Summary Overview",
                    chart_type="kpi_card",
                    x_axis=None,
                    y_axis=None,
                    reason="Quick snapshot of dataset volume and primary attributes.",
                )
            )

        AIObservabilityLogger.log_invocation("VisualizationAgent", "1.0", 150, 100, 35.0)

        return RecommendationResponse(
            recommended_widgets=widgets[: request.max_charts],
            suggested_layout={"columns": 12, "grid_gap": 16, "widgets_count": len(widgets)},
            filters=[d.source_column for d in dimensions[:3]],
        )

    async def generate_chart(self, user: User, workspace_id: uuid.UUID, dataset_id: uuid.UUID, request: ChartGenerateRequest) -> ChartGenerateResponse:
        dataset = await self.dataset_repo.get_for_user(dataset_id, user, workspace_id)
        if not dataset:
            raise ValueError("Dataset not found")

        if request.library == "plotly":
            spec: dict[str, Any] = {
                "data": [
                    {
                        "type": request.chart_type if request.chart_type != "kpi_card" else "indicator",
                        "x": [1, 2, 3, 4, 5],
                        "y": [10, 15, 13, 17, 22],
                        "marker": {"color": "#6366f1"},
                    }
                ],
                "layout": {
                    "title": f"{request.chart_type.title()} Chart for {dataset.name}",
                    "paper_bgcolor": "#1e1e2e",
                    "plot_bgcolor": "#1e1e2e",
                    "font": {"color": "#f3f4f6"},
                },
            }
        else:
            spec = {
                "title": {"text": f"{request.chart_type.title()} Chart - {dataset.name}"},
                "tooltip": {"trigger": "axis"},
                "xAxis": {"type": "category", "data": ["Mon", "Tue", "Wed", "Thu", "Fri"]},
                "yAxis": {"type": "value"},
                "series": [{"data": [820, 932, 901, 934, 1290], "type": request.chart_type}],
            }

        return ChartGenerateResponse(
            chart_type=request.chart_type,
            library=request.library,
            spec_json=spec,
            theme="modern_dark",
        )
