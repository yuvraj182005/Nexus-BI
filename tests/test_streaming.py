import time
import pytest
from app.streaming.schemas import StreamIngestEvent, WindowAggregationRequest
from app.streaming.service import global_streaming_engine


def test_streaming_ingest_and_window_aggregation():
    event1 = StreamIngestEvent(
        stream_topic="kafka_sales",
        event_type="kpi_update",
        data={"value": 1500.0},
        timestamp=time.time(),
    )
    event2 = StreamIngestEvent(
        stream_topic="kafka_sales",
        event_type="kpi_update",
        data={"value": 2500.0},
        timestamp=time.time(),
    )

    global_streaming_engine.ingest_event(event1)
    global_streaming_engine.ingest_event(event2)

    req = WindowAggregationRequest(metric_name="revenue", window_seconds=60, aggregation_func="sum")
    res = global_streaming_engine.compute_window_aggregation(req)
    assert res["value"] >= 4000.0
    assert res["samples_count"] >= 2


def test_streaming_status():
    status = global_streaming_engine.get_status()
    assert "kafka_sales_topic" in status.active_stream_topics
    assert status.ingested_events_count >= 2
