import time
import uuid
from typing import Any

from app.core.event_bus import global_event_bus
from app.core.observability import AIObservabilityLogger
from app.workflows.builder import global_workflow_builder
from app.workflows.schemas import WorkflowExecutionResponse


class WorkflowExecutor:
    @staticmethod
    async def execute(
        template_id: str, workspace_id: uuid.UUID, user_id: uuid.UUID, custom_params: dict[str, Any]
    ) -> WorkflowExecutionResponse:
        template = global_workflow_builder.get_template(template_id)
        if not template:
            raise ValueError(f"Workflow template '{template_id}' not found")

        execution_id = f"wf_exec_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        logs: list[str] = [f"[Workflow {execution_id}] Initialized template '{template.name}' v{template.version}"]
        step_results: list[dict[str, Any]] = []

        completed_count = 0
        for step in template.steps:
            step_start = time.time()
            logs.append(f"[{step.step_id}] Executing action: '{step.action}'")

            # Action simulation / engine hook
            res_data = {"step_id": step.step_id, "action": step.action, "status": "completed"}
            if step.action == "sql":
                res_data["sql"] = "SELECT * FROM dataset"
            elif step.action == "insights":
                res_data["insights_generated"] = 1

            completed_count += 1
            step_dur = (time.time() - step_start) * 1000.0
            res_data["duration_ms"] = round(step_dur, 2)
            step_results.append(res_data)

        total_dur = (time.time() - start_time) * 1000.0
        logs.append(f"[Workflow {execution_id}] All {completed_count} steps executed successfully.")

        AIObservabilityLogger.log_invocation("WorkflowExecutor", "1.0", 300, 200, total_dur)
        await global_event_bus.publish("WorkflowCompleted", {"execution_id": execution_id, "workspace_id": str(workspace_id)})

        return WorkflowExecutionResponse(
            execution_id=execution_id,
            template_id=template_id,
            status="completed",
            total_steps=len(template.steps),
            completed_steps=completed_count,
            duration_ms=round(total_dur, 2),
            step_results=step_results,
            logs=logs,
        )
