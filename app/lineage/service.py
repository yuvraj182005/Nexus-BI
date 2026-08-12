import uuid

from app.lineage.schemas import (
    ImpactAnalysisResponse,
    LineageEdge,
    LineageGraphResponse,
    LineageNode,
)


class LineageService:
    @staticmethod
    def get_lineage_graph(dataset_id: uuid.UUID) -> LineageGraphResponse:
        ds_id = str(dataset_id)
        nodes = [
            LineageNode(id=ds_id, label="Source Sales Dataset", node_type="dataset"),
            LineageNode(id=f"tx_{ds_id[:8]}", label="Imputation & Outlier Preprocessing", node_type="transformation"),
            LineageNode(id=f"sql_{ds_id[:8]}", label="Monthly Aggregation SQL Query", node_type="sql_query"),
            LineageNode(id=f"ana_{ds_id[:8]}", label="Revenue Trend EDA & Stats", node_type="analytics"),
            LineageNode(id=f"fc_{ds_id[:8]}", label="Arima 30-Day Sales Forecast", node_type="forecast"),
            LineageNode(id=f"ins_{ds_id[:8]}", label="Margin Expansion Insight", node_type="insight"),
            LineageNode(id=f"dash_{ds_id[:8]}", label="Executive KPI Dashboard", node_type="dashboard"),
            LineageNode(id=f"rep_{ds_id[:8]}", label="Q2 Executive Summary Report", node_type="report"),
            LineageNode(id=f"notif_{ds_id[:8]}", label="Slack Margin Alert", node_type="notification"),
        ]
        edges = [
            LineageEdge(source=ds_id, target=f"tx_{ds_id[:8]}"),
            LineageEdge(source=f"tx_{ds_id[:8]}", target=f"sql_{ds_id[:8]}"),
            LineageEdge(source=f"sql_{ds_id[:8]}", target=f"ana_{ds_id[:8]}"),
            LineageEdge(source=f"ana_{ds_id[:8]}", target=f"fc_{ds_id[:8]}"),
            LineageEdge(source=f"fc_{ds_id[:8]}", target=f"ins_{ds_id[:8]}"),
            LineageEdge(source=f"ins_{ds_id[:8]}", target=f"dash_{ds_id[:8]}"),
            LineageEdge(source=f"dash_{ds_id[:8]}", target=f"rep_{ds_id[:8]}"),
            LineageEdge(source=f"rep_{ds_id[:8]}", target=f"notif_{ds_id[:8]}"),
        ]
        return LineageGraphResponse(dataset_id=dataset_id, nodes=nodes, edges=edges)

    @staticmethod
    def analyze_deletion_impact(target_object_id: str, target_object_type: str) -> ImpactAnalysisResponse:
        affected_dashboards = [f"Dashboard_{target_object_id[:6]}", "Executive_Revenue_Summary"]
        affected_reports = [f"Report_{target_object_id[:6]}"]
        affected_workflows = ["Daily_Decision_Pipeline_v1"]
        affected_kpis = ["Gross_Margin_%", "Total_Sales_Revenue"]
        affected_datasets = ["Derived_Monthly_Summary"]

        total = len(affected_dashboards) + len(affected_reports) + len(affected_workflows) + len(affected_kpis) + len(affected_datasets)

        return ImpactAnalysisResponse(
            target_object_id=target_object_id,
            target_object_type=target_object_type,
            is_safe_to_delete=False,
            affected_datasets=affected_datasets,
            affected_dashboards=affected_dashboards,
            affected_reports=affected_reports,
            affected_workflows=affected_workflows,
            affected_kpis=affected_kpis,
            total_impacted_count=total,
        )


global_lineage_service = LineageService()
