from fastapi import APIRouter

from app.api.v1.agents import router as agent_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.audit import router as audit_router
from app.api.v1.auth import router as auth_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.chat import router as chat_router
from app.api.v1.collaboration import router as collaboration_router
from app.api.v1.connectors import router as connector_router
from app.api.v1.copilot import router as copilot_router
from app.api.v1.dashboards import router as dashboard_builder_router
from app.api.v1.datasets import router as dataset_router
from app.api.v1.forecasting import router as forecast_router
from app.api.v1.governance import router as governance_router
from app.api.v1.health import router as health_router
from app.api.v1.identity import router as identity_router
from app.api.v1.insights import router as insight_router
from app.api.v1.jobs import router as job_router
from app.api.v1.lineage import router as lineage_router
from app.api.v1.marketplace import router as marketplace_router
from app.api.v1.notifications import router as notification_router
from app.api.v1.observability import router as observability_router
from app.api.v1.plugins import router as plugin_router
from app.api.v1.preprocessing import router as preprocessing_router
from app.api.v1.profiling import router as profiling_router
from app.api.v1.reports import router as report_router
from app.api.v1.saas import router as saas_router
from app.api.v1.search import router as search_router
from app.api.v1.semantic import router as semantic_router
from app.api.v1.sql import router as sql_router
from app.api.v1.streaming import router as streaming_router
from app.api.v1.visualization import router as visualization_router
from app.api.v1.workflows import router as workflow_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, tags=["authentication"])
api_router.include_router(identity_router, tags=["identity"])
api_router.include_router(connector_router, tags=["connectors"])
api_router.include_router(dataset_router, tags=["datasets"])
api_router.include_router(profiling_router, tags=["profiling"])
api_router.include_router(preprocessing_router, tags=["preprocessing"])
api_router.include_router(semantic_router, tags=["semantic-layer"])
api_router.include_router(sql_router, tags=["sql-engine"])
api_router.include_router(analytics_router, tags=["analytics"])
api_router.include_router(forecast_router, tags=["forecasting"])
api_router.include_router(insight_router, tags=["insights"])
api_router.include_router(visualization_router, tags=["visualizations"])
api_router.include_router(agent_router, tags=["agents"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(report_router, tags=["reports"])
api_router.include_router(notification_router, tags=["notifications"])
api_router.include_router(workflow_router, tags=["workflows"])
api_router.include_router(job_router, tags=["jobs"])
api_router.include_router(catalog_router, tags=["catalog"])
api_router.include_router(governance_router, tags=["governance"])
api_router.include_router(audit_router, tags=["audit"])
api_router.include_router(plugin_router, tags=["plugins"])
api_router.include_router(observability_router, tags=["observability"])
api_router.include_router(collaboration_router, tags=["collaboration"])
api_router.include_router(streaming_router, tags=["streaming"])
api_router.include_router(copilot_router, tags=["copilot"])
api_router.include_router(dashboard_builder_router, tags=["dashboards"])
api_router.include_router(lineage_router, tags=["lineage"])
api_router.include_router(search_router, tags=["search"])
api_router.include_router(saas_router, tags=["saas"])
api_router.include_router(marketplace_router, tags=["marketplace"])
