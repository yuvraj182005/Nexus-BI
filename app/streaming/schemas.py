from typing import Any

from pydantic import BaseModel, Field


class StreamIngestEvent(BaseModel):
    stream_topic: str = Field(..., description="kafka, redis_stream, rabbitmq, telemetry")
    event_type: str  # kpi_update, live_sql_result, forecast_update, notification
    data: dict[str, Any]
    timestamp: float


class WindowAggregationRequest(BaseModel):
    metric_name: str
    window_seconds: int = Field(60, ge=5, le=3600)
    aggregation_func: str = Field("sum", description="sum, avg, count, max, min")


class StreamingStatusResponse(BaseModel):
    active_stream_topics: list[str]
    ingested_events_count: int
    backpressure_queue_size: int
    reconnect_attempts: int
    avg_latency_ms: float
