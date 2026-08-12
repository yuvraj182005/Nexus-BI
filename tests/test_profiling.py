import pandas as pd

from app.services.profiling import ProfilingService


def test_profile_frame_calculates_quality_and_column_metrics() -> None:
    frame = pd.DataFrame(
        {
            "customer_id": [1, 2, 2, 4],
            "revenue": [100.0, 200.0, None, 5000.0],
            "order_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        }
    )

    report = ProfilingService._profile_frame(frame)

    assert report["rows"] == 4
    assert report["columns"] == 3
    assert report["missing_values"] == 1
    assert report["duplicate_rows"] == 0
    assert 0 <= report["overall_health_score"] <= 100
    assert any(column["name"] == "order_date" and "date_summary" in column for column in report["column_profiles"])
    assert any(relationship["column"] == "customer_id" for relationship in report["relationships"])
    assert "metrics" in report["report_json"]
    assert "report_json" not in report["report_json"]["metrics"]


def test_profile_frame_handles_empty_numeric_input() -> None:
    report = ProfilingService._profile_frame(pd.DataFrame({"value": []}))

    assert report["rows"] == 0
    assert report["columns"] == 1
    assert report["correlations"] == {}
