import uuid
from typing import Any

from pydantic import BaseModel, Field


class CopilotRequest(BaseModel):
    user_prompt: str = Field(..., description="Natural language prompt e.g. 'Generate executive sales dashboard for Q2'")
    context_type: str = Field("all", description="sql, dashboard, report, kpi, cleaning, forecast, presentation, workflow, all")
    dataset_id: uuid.UUID | None = None
    session_id: str | None = None


class CopilotActionStep(BaseModel):
    step_number: int
    action_type: str  # generate_sql, generate_dashboard, generate_report, explain_kpi, recommend_cleaning, suggest_forecast, suggest_workflow
    title: str
    output_payload: dict[str, Any]


class CopilotResponse(BaseModel):
    session_id: str
    summary_insight: str
    plan_steps: list[CopilotActionStep]
    suggested_followups: list[str]
