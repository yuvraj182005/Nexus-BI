import uuid
from typing import Any

from pydantic import BaseModel, Field


class LineageNode(BaseModel):
    id: str
    label: str
    node_type: str  # dataset, transformation, sql_query, analytics, forecast, insight, dashboard, report, notification
    metadata: dict[str, Any] = Field(default_factory=dict)


class LineageEdge(BaseModel):
    source: str
    target: str
    relationship_type: str = "derives_from"


class LineageGraphResponse(BaseModel):
    dataset_id: uuid.UUID
    nodes: list[LineageNode]
    edges: list[LineageEdge]


class ImpactAnalysisResponse(BaseModel):
    target_object_id: str
    target_object_type: str
    is_safe_to_delete: bool
    affected_datasets: list[str]
    affected_dashboards: list[str]
    affected_reports: list[str]
    affected_workflows: list[str]
    affected_kpis: list[str]
    total_impacted_count: int
