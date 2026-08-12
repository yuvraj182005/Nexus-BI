import uuid
import pytest
from app.copilot.schemas import CopilotRequest
from app.copilot.service import global_copilot_service


@pytest.mark.asyncio
async def test_copilot_multi_step_planning():
    u_id = uuid.uuid4()
    ws_id = uuid.uuid4()
    req = CopilotRequest(
        user_prompt="Generate executive sales dashboard for Q2 and suggest forecast model",
        context_type="all",
    )

    res = await global_copilot_service.execute_copilot(u_id, ws_id, req)
    assert res.session_id is not None
    assert len(res.plan_steps) == 4
    assert res.plan_steps[0].action_type == "recommend_cleaning"
    assert len(res.suggested_followups) >= 1
