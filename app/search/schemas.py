from typing import Any

from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    id: str
    entity_type: str  # dataset, dashboard, report, insight, workflow, sql, user, glossary, kpi, plugin
    title: str
    description: str
    tags: list[str]
    relevance_score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class GlobalSearchRequest(BaseModel):
    query: str
    entity_types: list[str] | None = None
    tags: list[str] | None = None
    use_semantic: bool = True
    limit: int = Field(20, ge=1, le=100)


class GlobalSearchResponse(BaseModel):
    query: str
    total_matches: int
    facets: dict[str, int]
    items: list[SearchResultItem]
    recommendations: list[SearchResultItem]


class SavedSearchCreateRequest(BaseModel):
    name: str
    query: str
    filters: dict[str, Any] = Field(default_factory=dict)
