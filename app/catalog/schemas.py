from typing import Any

from pydantic import BaseModel, Field


class CatalogItem(BaseModel):
    id: str
    entity_type: str  # dataset, dashboard, report, kpi, workflow, model
    name: str
    description: str
    tags: list[str]
    owner: str
    business_domain: str
    popularity_score: float = 0.0
    views_count: int = 0
    is_starred: bool = False
    is_favorite: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class CatalogSearchRequest(BaseModel):
    query: str | None = None
    entity_types: list[str] | None = None
    business_domains: list[str] | None = None
    tags: list[str] | None = None
    starred_only: bool = False
    sort_by: str = Field("popularity", description="popularity, name, recent")


class CatalogSearchResponse(BaseModel):
    total_matches: int
    items: list[CatalogItem]
    recommendations: list[CatalogItem]
