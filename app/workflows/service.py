import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.models.identity import User
from app.workflows.builder import global_workflow_builder
from app.workflows.scheduler import WorkflowScheduler
from app.workflows.schemas import (
    WorkflowExecuteRequest,
    WorkflowExecutionResponse,
    WorkflowTemplate,
)


class WorkflowService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.scheduler = WorkflowScheduler()

    async def list_templates(self) -> list[WorkflowTemplate]:
        return global_workflow_builder.list_templates()

    async def execute_workflow(self, user: User, workspace_id: uuid.UUID, request: WorkflowExecuteRequest) -> WorkflowExecutionResponse:
        return await self.scheduler.trigger_manual(request.template_id, workspace_id, user.id, request.custom_params)
