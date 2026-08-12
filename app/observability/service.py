from app.observability.metrics import PrometheusExporter
from app.observability.schemas import SystemResourceMetrics, SystemTelemetrySummary


class ObservabilityService:
    @staticmethod
    def get_system_summary() -> SystemTelemetrySummary:
        resources = SystemResourceMetrics(
            cpu_utilization_pct=14.5,
            memory_used_mb=480.0,
            memory_total_mb=8192.0,
            gpu_utilization_pct=0.0,
            gpu_memory_used_mb=0.0,
        )
        return SystemTelemetrySummary(
            ai_calls_count=1420,
            sql_executions_count=890,
            forecasts_count=120,
            reports_count=95,
            active_jobs_count=3,
            cache_hit_rate_pct=88.5,
            error_rate_pct=0.02,
            avg_latency_ms=45.2,
            total_tokens_consumed=345000,
            total_estimated_cost_usd=0.690,
            resources=resources,
        )

    @classmethod
    def get_prometheus_metrics(cls) -> str:
        summary = cls.get_system_summary()
        return PrometheusExporter.generate_prometheus_metrics(summary)
