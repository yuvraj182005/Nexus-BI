import uuid
import pytest
from app.audit.service import global_audit_service


@pytest.mark.asyncio
async def test_audit_recording_and_search():
    u_id = uuid.uuid4()
    ws_id = uuid.uuid4()

    global_audit_service.record_activity(
        user_id=u_id,
        workspace_id=ws_id,
        action="dataset_upload",
        target="sales_q2.csv",
        duration_ms=120.0,
    )

    req = await global_audit_service.search_logs(ws_id, type("Req", (), {"user_id": None, "actions": None, "status_filter": None, "limit": 10})())
    assert req.total_count >= 1
    assert req.logs[0].action == "dataset_upload"
    assert req.logs[0].target == "sales_q2.csv"
