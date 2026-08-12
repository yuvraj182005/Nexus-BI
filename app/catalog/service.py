import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.catalog.schemas import CatalogItem, CatalogSearchRequest, CatalogSearchResponse
from app.core.config import Settings


class DataCatalogService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self._seed_catalog()

    def _seed_catalog(self) -> None:
        self.catalog: list[CatalogItem] = [
            CatalogItem(
                id="cat_ds_1",
                entity_type="dataset",
                name="Sales & Financial Performance Q2",
                description="Core revenue, profit margin, and transaction dataset",
                tags=["sales", "revenue", "finance"],
                owner="Finance Lead",
                business_domain="Sales",
                popularity_score=98.5,
                views_count=340,
                is_starred=True,
                is_favorite=True,
            ),
            CatalogItem(
                id="cat_dash_1",
                entity_type="dashboard",
                name="Executive Revenue Dashboard",
                description="Interactive Plotly KPIs and temporal trend charts",
                tags=["executive", "kpi", "dashboard"],
                owner="BI Analyst",
                business_domain="Sales",
                popularity_score=92.0,
                views_count=210,
                is_starred=True,
            ),
            CatalogItem(
                id="cat_rep_1",
                entity_type="report",
                name="Q2 Executive Summary Report",
                description="Markdown and HTML rendered executive summary",
                tags=["report", "executive"],
                owner="Chief Data Officer",
                business_domain="Executive",
                popularity_score=85.0,
                views_count=150,
            ),
            CatalogItem(
                id="cat_kpi_1",
                entity_type="kpi",
                name="Gross Profit Margin %",
                description="Calculated gross margin across all business lines",
                tags=["kpi", "profit", "margin"],
                owner="Finance Lead",
                business_domain="Finance",
                popularity_score=99.0,
                views_count=520,
                is_starred=True,
            ),
            CatalogItem(
                id="cat_wf_1",
                entity_type="workflow",
                name="End-to-End Decision Intelligence Pipeline",
                description="Automated 12-stage decision pipeline",
                tags=["workflow", "automation"],
                owner="MLOps Engineer",
                business_domain="Operations",
                popularity_score=90.0,
                views_count=180,
            ),
        ]

    async def search(self, workspace_id: uuid.UUID, request: CatalogSearchRequest) -> CatalogSearchResponse:
        results = list(self.catalog)

        if request.starred_only:
            results = [item for item in results if item.is_starred]

        if request.entity_types:
            results = [item for item in results if item.entity_type in request.entity_types]

        if request.business_domains:
            results = [item for item in results if item.business_domain in request.business_domains]

        if request.query:
            q = request.query.lower()
            results = [
                item for item in results
                if q in item.name.lower() or q in item.description.lower() or any(q in t.lower() for t in item.tags)
            ]

        if request.sort_by == "popularity":
            results.sort(key=lambda x: x.popularity_score, reverse=True)
        elif request.sort_by == "name":
            results.sort(key=lambda x: x.name.lower())

        recommendations = [item for item in self.catalog if item.popularity_score > 90.0][:2]

        return CatalogSearchResponse(
            total_matches=len(results),
            items=results,
            recommendations=recommendations,
        )

    async def toggle_star(self, item_id: str) -> CatalogItem:
        for item in self.catalog:
            if item.id == item_id:
                item.is_starred = not item.is_starred
                return item
        raise ValueError(f"Catalog item '{item_id}' not found")
