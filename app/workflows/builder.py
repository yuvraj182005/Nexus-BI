from app.workflows.schemas import WorkflowStepConfig, WorkflowTemplate


class WorkflowBuilder:
    def __init__(self) -> None:
        self._templates: dict[str, WorkflowTemplate] = {}
        self._register_default_templates()

    def _register_default_templates(self) -> None:
        end_to_end = WorkflowTemplate(
            template_id="end_to_end_analytics",
            name="Complete Decision Intelligence Pipeline",
            description="Runs upload -> profile -> clean -> semantic -> sql -> analytics -> forecast -> insights -> dashboard -> report -> notification -> archive",
            version="1.0.0",
            steps=[
                WorkflowStepConfig(step_id="s1", action="upload"),
                WorkflowStepConfig(step_id="s2", action="profile"),
                WorkflowStepConfig(step_id="s3", action="clean"),
                WorkflowStepConfig(step_id="s4", action="semantic"),
                WorkflowStepConfig(step_id="s5", action="sql"),
                WorkflowStepConfig(step_id="s6", action="analytics"),
                WorkflowStepConfig(step_id="s7", action="forecast"),
                WorkflowStepConfig(step_id="s8", action="insights"),
                WorkflowStepConfig(step_id="s9", action="dashboard"),
                WorkflowStepConfig(step_id="s10", action="report"),
                WorkflowStepConfig(step_id="s11", action="notification"),
                WorkflowStepConfig(step_id="s12", action="archive"),
            ],
        )
        self._templates[end_to_end.template_id] = end_to_end

    def register_template(self, template: WorkflowTemplate) -> None:
        self._templates[template.template_id] = template

    def get_template(self, template_id: str) -> WorkflowTemplate | None:
        return self._templates.get(template_id)

    def list_templates(self) -> list[WorkflowTemplate]:
        return list(self._templates.values())


global_workflow_builder = WorkflowBuilder()
