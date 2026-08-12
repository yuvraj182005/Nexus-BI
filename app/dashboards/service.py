import time
import uuid
from typing import Any

from app.dashboards.schemas import (
    DashboardCreateRequest,
    DashboardDetailResponse,
    DashboardGridWidget,
    DashboardSnapshotResponse,
)


class DashboardBuilderService:
    TEMPLATES = {
        "exec_kpi_summary": {
            "title": "Executive KPI Summary Template",
            "widgets": [
                {"title": "Total Revenue KPI", "chart_type": "kpi_card", "x": 0, "y": 0, "w": 3, "h": 2},
                {"title": "Gross Profit Margin", "chart_type": "kpi_card", "x": 3, "y": 0, "w": 3, "h": 2},
                {"title": "Monthly Revenue Trend", "chart_type": "line", "x": 0, "y": 2, "w": 6, "h": 4},
                {"title": "Regional Sales Share", "chart_type": "pie", "x": 6, "y": 0, "w": 6, "h": 6},
            ],
        }
    }

    def __init__(self) -> None:
        self._dashboards: dict[str, DashboardDetailResponse] = {}

    def create_dashboard(self, workspace_id: uuid.UUID, request: DashboardCreateRequest) -> DashboardDetailResponse:
        d_id = f"dash_{uuid.uuid4().hex[:10]}"
        widgets = request.widgets

        if request.template_id and request.template_id in self.TEMPLATES:
            tpl = self.TEMPLATES[request.template_id]
            for w in tpl["widgets"]:
                widgets.append(
                    DashboardGridWidget(
                        title=w["title"],
                        chart_type=w["chart_type"],
                        x=w["x"],
                        y=w["y"],
                        w=w["w"],
                        h=w["h"],
                    )
                )

        detail = DashboardDetailResponse(
            id=d_id,
            workspace_id=workspace_id,
            title=request.title,
            description=request.description,
            theme=request.theme,
            version=1,
            widgets=widgets,
            global_filters=request.global_filters,
            bookmarks=[],
            is_public_shared=False,
            embed_url=f"/embed/dashboards/{d_id}",
            created_at=time.time(),
        )
        self._dashboards[d_id] = detail
        return detail

    def generate_snapshot(self, dashboard_id: str) -> DashboardSnapshotResponse:
        if dashboard_id not in self._dashboards:
            raise ValueError(f"Dashboard '{dashboard_id}' not found")
        return DashboardSnapshotResponse(
            snapshot_id=f"snap_{uuid.uuid4().hex[:8]}",
            dashboard_id=dashboard_id,
            rendered_image_url=f"/exports/dashboards/{dashboard_id}_snapshot.png",
            pdf_export_url=f"/exports/dashboards/{dashboard_id}_export.pdf",
            timestamp=time.time(),
        )

    def add_bookmark(self, dashboard_id: str, bookmark_name: str, filter_state: dict[str, Any]) -> DashboardDetailResponse:
        if dashboard_id not in self._dashboards:
            raise ValueError(f"Dashboard '{dashboard_id}' not found")
        d = self._dashboards[dashboard_id]
        d.bookmarks.append({"name": bookmark_name, "filters": filter_state, "created_at": time.time()})
        return d


global_dashboard_builder = DashboardBuilderService()
