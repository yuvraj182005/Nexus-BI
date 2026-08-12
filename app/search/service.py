import time
import uuid
from typing import Any

from app.search.schemas import (
    GlobalSearchRequest,
    GlobalSearchResponse,
    SavedSearchCreateRequest,
    SearchResultItem,
)


class GlobalSearchService:
    def __init__(self) -> None:
        self._seed_search_index()
        self._recent_searches: list[str] = []
        self._saved_searches: list[dict[str, Any]] = []

    def _seed_search_index(self) -> None:
        self.index: list[SearchResultItem] = [
            SearchResultItem(id="ds_1", entity_type="dataset", title="Sales & Revenue Q2", description="Core transactional revenue dataset", tags=["sales", "finance"], relevance_score=0.98),
            SearchResultItem(id="dash_1", entity_type="dashboard", title="Executive Revenue Dashboard", description="Plotly KPIs & trends", tags=["executive", "kpi"], relevance_score=0.95),
            SearchResultItem(id="rep_1", entity_type="report", title="Q2 Executive Summary Report", description="Rendered executive report", tags=["report"], relevance_score=0.90),
            SearchResultItem(id="ins_1", entity_type="insight", title="Margin Expansion Anomaly Insight", description="Business ROI insight", tags=["insight"], relevance_score=0.88),
            SearchResultItem(id="wf_1", entity_type="workflow", title="End-to-End Decision Pipeline", description="12-stage workflow", tags=["workflow"], relevance_score=0.85),
            SearchResultItem(id="sql_1", entity_type="sql", title="Monthly Regional Aggregation Query", description="SELECT category, SUM(revenue)...", tags=["sql"], relevance_score=0.82),
            SearchResultItem(id="usr_1", entity_type="user", title="Alice Chief Analyst", description="Lead BI Analyst", tags=["user"], relevance_score=0.80),
            SearchResultItem(id="gls_1", entity_type="glossary", title="Gross Profit Margin", description="Financial metric definition", tags=["glossary"], relevance_score=0.99),
            SearchResultItem(id="kpi_1", entity_type="kpi", title="Gross Profit Margin %", description="Calculated KPI", tags=["kpi"], relevance_score=0.97),
            SearchResultItem(id="plg_1", entity_type="plugin", title="Partner DeepAR Forecaster", description="Custom ML plugin", tags=["plugin"], relevance_score=0.78),
        ]

    def search(self, request: GlobalSearchRequest) -> GlobalSearchResponse:
        self._recent_searches.append(request.query)
        q = request.query.lower()
        matched = []

        for item in self.index:
            if request.entity_types and item.entity_type not in request.entity_types:
                continue
            if request.tags and not any(t in item.tags for t in request.tags):
                continue
            if q in item.title.lower() or q in item.description.lower() or any(q in t for t in item.tags):
                matched.append(item)

        matched.sort(key=lambda x: x.relevance_score, reverse=True)

        # Build facets
        facets: dict[str, int] = {}
        for m in matched:
            facets[m.entity_type] = facets.get(m.entity_type, 0) + 1

        recommendations = [item for item in self.index if item.relevance_score > 0.90][:2]

        return GlobalSearchResponse(
            query=request.query,
            total_matches=len(matched),
            facets=facets,
            items=matched[: request.limit],
            recommendations=recommendations,
        )

    def save_search(self, request: SavedSearchCreateRequest) -> dict[str, Any]:
        item = {"id": uuid.uuid4().hex[:8], "name": request.name, "query": request.query, "created_at": time.time()}
        self._saved_searches.append(item)
        return item

    def get_search_history(self) -> list[str]:
        return list(reversed(self._recent_searches[-20:]))


global_search_service = GlobalSearchService()
