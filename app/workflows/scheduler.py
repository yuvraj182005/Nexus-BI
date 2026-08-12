import uuid
from typing import Any

from app.workflows.executor import WorkflowExecutor
from app.workflows.schemas import WorkflowExecutionResponse


class WorkflowScheduler:
    def __init__(self) -> None:
        self._schedules: dict[str, dict[str, Any]] = {}

    def schedule_cron(self, schedule_id: str, template_id: str, cron_expr: str, workspace_id: uuid.UUID) -> dict[str, Any]:
        spec = {
            "schedule_id": schedule_id,
            "template_id": template_id,
            "cron": cron_expr,
            "workspace_id": str(workspace_id),
            "status": "active",
        }
        self._schedules[schedule_id] = spec
        return spec

    async def trigger_manual(self, template_id: str, workspace_id: uuid.UUID, user_id: uuid.UUID, custom_params: dict[str, Any]) -> WorkflowExecutionResponse:
        return await WorkflowExecutor.execute(template_id, workspace_id, user_id, custom_params)
