from typing import Any

from pydantic import BaseModel, Field


class PluginManifest(BaseModel):
    plugin_id: str = Field(..., description="Unique plugin ID e.g. custom_snowflake_v2")
    name: str
    version: str = "1.0.0"
    plugin_type: str = Field(..., description="connector, visualization, forecast, analytics, ai, notification, workflow")
    author: str
    permissions: list[str] = Field(default_factory=lambda: ["read_dataset", "execute_query"])
    config_schema: dict[str, Any] = Field(default_factory=dict)
    entry_point: str = Field("main:PluginHandler")
    is_active: bool = True


class PluginRegisterRequest(BaseModel):
    manifest: PluginManifest
    code: str = Field(..., description="Python source code or module definition")
