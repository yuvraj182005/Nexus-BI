import uuid
import pytest
from app.lineage.service import global_lineage_service


def test_lineage_graph_structure():
    ds_id = uuid.uuid4()
    graph = global_lineage_service.get_lineage_graph(ds_id)
    assert graph.dataset_id == ds_id
    assert len(graph.nodes) == 9
    assert len(graph.edges) == 8


def test_impact_analysis():
    impact = global_lineage_service.analyze_deletion_impact("ds_sales_q2", "dataset")
    assert impact.is_safe_to_delete is False
    assert impact.total_impacted_count > 0
    assert "Executive_Revenue_Summary" in impact.affected_dashboards
