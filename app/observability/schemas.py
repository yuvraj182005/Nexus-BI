from pydantic import BaseModel


class SystemResourceMetrics(BaseModel):
    cpu_utilization_pct: float
    memory_used_mb: float
    memory_total_mb: float
    gpu_utilization_pct: float | None = None
    gpu_memory_used_mb: float | None = None


class SystemTelemetrySummary(BaseModel):
    ai_calls_count: int
    sql_executions_count: int
    forecasts_count: int
    reports_count: int
    active_jobs_count: int
    cache_hit_rate_pct: float
    error_rate_pct: float
    avg_latency_ms: float
    total_tokens_consumed: int
    total_estimated_cost_usd: float
    resources: SystemResourceMetrics
