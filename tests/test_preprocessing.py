import pandas as pd

from app.models.preprocessing import PreprocessingOperation, PreprocessingStepDecision
from app.schemas.preprocessing import PreprocessingStepRequest
from app.services.preprocessing import PreprocessingService


def test_recommendations_detect_missing_duplicates_dates_and_outliers() -> None:
    frame = pd.DataFrame(
        {
            "Customer ID": [1, 1, 3, 4],
            "Revenue": [100.0, 100.0, None, 5000.0],
            "Order Date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        }
    )

    recommendations = PreprocessingService._recommend_frame(frame)
    operations = {recommendation["operation"] for recommendation in recommendations}

    assert PreprocessingOperation.DROP_DUPLICATES in operations
    assert PreprocessingOperation.IMPUTE_MISSING in operations
    assert PreprocessingOperation.PARSE_DATES in operations
    assert PreprocessingOperation.STANDARDIZE_COLUMNS in operations


def test_transformations_are_deterministic_and_do_not_mutate_input() -> None:
    original = pd.DataFrame({"Revenue": [10.0, None], "Units": [2.0, 4.0]})
    request = PreprocessingStepRequest(
        operation=PreprocessingOperation.IMPUTE_MISSING,
        column_name="Revenue",
        decision=PreprocessingStepDecision.CUSTOMIZED,
        parameters={"method": "median"},
    )

    transformed = PreprocessingService._apply_operation(original.copy(), request)

    assert original["Revenue"].isna().sum() == 1
    assert transformed["Revenue"].isna().sum() == 0
    assert transformed["Revenue"].tolist() == [10.0, 10.0]


def test_safe_derived_ratio_rejects_missing_parameters() -> None:
    request = PreprocessingStepRequest(
        operation=PreprocessingOperation.DERIVE_RATIO,
        parameters={},
    )

    try:
        PreprocessingService._apply_operation(pd.DataFrame({"a": [1]}), request)
    except ValueError as exc:
        assert "derive_ratio" in str(exc)
    else:
        raise AssertionError("Expected invalid derived-ratio configuration to fail")
