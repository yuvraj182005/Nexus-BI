import pytest
from app.observability.service import ObservabilityService


def test_observability_summary_and_prometheus():
    summary = ObservabilityService.get_system_summary()
    assert summary.ai_calls_count > 0
    assert summary.resources.cpu_utilization_pct >= 0.0

    prom_text = ObservabilityService.get_prometheus_metrics()
    assert "nexusbi_ai_calls_total" in prom_text
    assert "nexusbi_cpu_utilization_percent" in prom_text
