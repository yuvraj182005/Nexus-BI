import uuid
from typing import Any

from pydantic import BaseModel, Field


class AgentWorkflowRequest(BaseModel):
    dataset_id: uuid.UUID = Field(..., description="Target dataset ID")
    user_prompt: str = Field(..., description="High-level goal prompt for multi-agent system")
    enabled_agents: list[str] | None = Field(
        None,
        description="List of agents to run (data_engineer, sql, analytics, forecast, visualization, insight, report, notification)",
    )


class AgentStepResult(BaseModel):
    agent_name: str
    status: str
    duration_ms: float
    output: dict[str, Any]
    logs: list[str]


class AgentWorkflowResponse(BaseModel):
    workflow_id: str
    user_prompt: str
    overall_status: str
    total_duration_ms: float
    steps: list[AgentStepResult]
    final_artifact_summary: str
