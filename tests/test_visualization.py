import pytest
from app.visualization.schemas import ChartGenerateRequest


def test_chart_generate_schema():
    req = ChartGenerateRequest(chart_type="bar", library="echarts")
    assert req.chart_type == "bar"
    assert req.library == "echarts"
