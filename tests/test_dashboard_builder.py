import uuid
import pytest
from app.dashboards.schemas import DashboardCreateRequest
from app.dashboards.service import global_dashboard_builder


def test_dashboard_builder_template_and_snapshots():
    ws_id = uuid.uuid4()
    req = DashboardCreateRequest(
        title="Q2 Executive Sales Dashboard",
        theme="dark_glassmorphism",
        template_id="exec_kpi_summary",
    )
    detail = global_dashboard_builder.create_dashboard(ws_id, req)
    assert detail.id.startswith("dash_")
    assert len(detail.widgets) == 4
    assert detail.embed_url.startswith("/embed/dashboards/")

    snap = global_dashboard_builder.generate_snapshot(detail.id)
    assert snap.snapshot_id.startswith("snap_")
    assert snap.pdf_export_url.endswith(".pdf")
