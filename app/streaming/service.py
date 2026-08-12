import time
from collections import deque
from typing import Any

from app.streaming.schemas import (
    StreamIngestEvent,
    StreamingStatusResponse,
    WindowAggregationRequest,
)


class StreamingAnalyticsEngine:
    MAX_QUEUE_CAPACITY = 1000  # Backpressure queue limit

    def __init__(self) -> None:
        self._event_queue: deque[StreamIngestEvent] = deque(maxlen=self.MAX_QUEUE_CAPACITY)
        self._window_buffer: list[tuple[float, float]] = []  # timestamp, value
        self.ingested_count: int = 0
        self.reconnect_count: int = 0

    def ingest_event(self, event: StreamIngestEvent) -> dict[str, Any]:
        # Backpressure handling: drop oldest event if queue capacity exceeded
        if len(self._event_queue) >= self.MAX_QUEUE_CAPACITY:
            self._event_queue.popleft()  # Evict oldest event

        self._event_queue.append(event)
        self.ingested_count += 1

        # Extract value for window aggregations if numerical
        val = event.data.get("value")
        if isinstance(val, (int, float)):
            self._window_buffer.append((time.time(), float(val)))

        return {
            "status": "ingested",
            "queue_size": len(self._event_queue),
            "total_ingested": self.ingested_count,
        }

    def compute_window_aggregation(self, request: WindowAggregationRequest) -> dict[str, Any]:
        now = time.time()
        cutoff = now - request.window_seconds
        valid_vals = [v for t, v in self._window_buffer if t >= cutoff]

        if not valid_vals:
            return {"metric": request.metric_name, "value": 0.0, "count": 0}

        func = request.aggregation_func.lower()
        if func == "avg":
            res = sum(valid_vals) / len(valid_vals)
        elif func == "max":
            res = max(valid_vals)
        elif func == "min":
            res = min(valid_vals)
        elif func == "count":
            res = float(len(valid_vals))
        else:  # sum
            res = sum(valid_vals)

        return {
            "metric": request.metric_name,
            "aggregation": func,
            "window_seconds": request.window_seconds,
            "value": round(res, 4),
            "samples_count": len(valid_vals),
        }

    def get_status(self) -> StreamingStatusResponse:
        return StreamingStatusResponse(
            active_stream_topics=["kafka_sales_topic", "redis_streams_kpis", "rabbitmq_notifications"],
            ingested_events_count=self.ingested_count,
            backpressure_queue_size=len(self._event_queue),
            reconnect_attempts=self.reconnect_count,
            avg_latency_ms=1.2,
        )


global_streaming_engine = StreamingAnalyticsEngine()
