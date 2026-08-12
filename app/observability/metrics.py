from app.observability.schemas import SystemTelemetrySummary


class PrometheusExporter:
    @staticmethod
    def generate_prometheus_metrics(summary: SystemTelemetrySummary) -> str:
        lines = [
            "# HELP nexusbi_ai_calls_total Total count of AI Gateway LLM calls",
            "# TYPE nexusbi_ai_calls_total counter",
            f"nexusbi_ai_calls_total {summary.ai_calls_count}",
            "# HELP nexusbi_sql_executions_total Total count of SQL queries executed",
            "# TYPE nexusbi_sql_executions_total counter",
            f"nexusbi_sql_executions_total {summary.sql_executions_count}",
            "# HELP nexusbi_avg_latency_milliseconds Average request latency",
            "# TYPE nexusbi_avg_latency_milliseconds gauge",
            f"nexusbi_avg_latency_milliseconds {summary.avg_latency_ms}",
            "# HELP nexusbi_total_tokens_consumed Total LLM tokens consumed",
            "# TYPE nexusbi_total_tokens_consumed counter",
            f"nexusbi_total_tokens_consumed {summary.total_tokens_consumed}",
            "# HELP nexusbi_total_cost_dollars Estimated cost in USD",
            "# TYPE nexusbi_total_cost_dollars counter",
            f"nexusbi_total_cost_dollars {summary.total_estimated_cost_usd:.6f}",
            "# HELP nexusbi_cpu_utilization_percent CPU utilization percentage",
            "# TYPE nexusbi_cpu_utilization_percent gauge",
            f"nexusbi_cpu_utilization_percent {summary.resources.cpu_utilization_pct}",
        ]
        return "\n".join(lines) + "\n"
