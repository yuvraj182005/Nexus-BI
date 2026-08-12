import time
import uuid
from typing import Any

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    category: str = Field(..., description="dataset, sql, dashboard, report, insight, chat, user_pref, workspace_pref")
    workspace_id: uuid.UUID
    user_id: uuid.UUID | None = None
    session_id: str | None = None
    key: str
    value: dict[str, Any]
    created_at: float = Field(default_factory=time.time)
    ttl_seconds: float = Field(3600.0, description="Time to live in seconds")

    @property
    def is_expired(self) -> bool:
        return time.time() > (self.created_at + self.ttl_seconds)


class UserPreferences(BaseModel):
    user_id: uuid.UUID
    preferred_dialect: str = "duckdb"
    preferred_chart_library: str = "plotly"
    preferred_theme: str = "modern_dark"


class WorkspacePreferences(BaseModel):
    workspace_id: uuid.UUID
    default_ai_provider: str = "openai"
    max_forecast_horizon: int = 12
    enable_auto_profiling: bool = True
