from typing import Any

from pydantic import BaseModel


class EDARequest(BaseModel):
    target_columns: list[str] | None = None


class EDAResponse(BaseModel):
    detected_domain: str
    row_count: int
    column_count: int
    descriptive_stats: dict[str, Any]
    correlation_matrix: dict[str, dict[str, float]]
    outlier_summary: dict[str, int]
    insights_summary: list[str]
