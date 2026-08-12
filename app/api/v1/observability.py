from fastapi import APIRouter, Response

from app.observability.schemas import SystemTelemetrySummary
from app.observability.service import ObservabilityService

router = APIRouter()


@router.get("/metrics")
async def get_prometheus_metrics() -> Response:
    metrics_text = ObservabilityService.get_prometheus_metrics()
    return Response(content=metrics_text, media_type="text/plain; version=0.0.4")


@router.get("/observability/summary", response_model=SystemTelemetrySummary)
async def get_observability_summary() -> SystemTelemetrySummary:
    return ObservabilityService.get_system_summary()
