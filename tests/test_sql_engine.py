import pytest
import pandas as pd
from app.sql_engine.executor import SQLExecutor
from app.sql_engine.validators import SQLValidator


def test_sql_validator_safe():
    is_safe, error = SQLValidator.validate_read_only("SELECT * FROM users WHERE active = true")
    assert is_safe is True
    assert error is None


def test_sql_validator_reject_dangerous():
    is_safe, error = SQLValidator.validate_read_only("DROP TABLE users;")
    assert is_safe is False
    assert "Dangerous operation" in error


def test_sql_executor_duckdb():
    df = pd.DataFrame({"id": [1, 2], "revenue": [100.0, 200.0]})
    cols, rows, elapsed = SQLExecutor.execute_on_dataframe(df, "sales_data", "SELECT * FROM sales_data")
    assert cols == ["id", "revenue"]
    assert len(rows) == 2
    assert elapsed >= 0.0
