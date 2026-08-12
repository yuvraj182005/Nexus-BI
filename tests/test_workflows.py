import uuid
import pytest
from app.workflows.builder import global_workflow_builder
from app.workflows.executor import WorkflowExecutor


@pytest.mark.asyncio
async def test_workflow_template_registry():
    templates = global_workflow_builder.list_templates()
    assert len(templates) >= 1
    assert templates[0].template_id == "end_to_end_analytics"
    assert len(templates[0].steps) == 12


@pytest.mark.asyncio
async def test_workflow_executor():
    ws_id = uuid.uuid4()
    u_id = uuid.uuid4()
    res = await WorkflowExecutor.execute("end_to_end_analytics", ws_id, u_id, {})
    assert res.status == "completed"
    assert res.total_steps == 12
    assert res.completed_steps == 12
    assert len(res.logs) >= 13
