import time
from typing import Any

import duckdb
import pandas as pd


class SQLExecutor:
    @staticmethod
    def execute_on_dataframe(df: pd.DataFrame, table_name: str, sql: str, limit: int = 100) -> tuple[list[str], list[dict[str, Any]], float]:
        start_time = time.time()
        con = duckdb.connect(database=":memory:")
        con.register(table_name, df)
        
        adjusted_sql = sql.strip()
        if "LIMIT" not in adjusted_sql.upper():
            adjusted_sql = f"{adjusted_sql} LIMIT {limit}"
            
        res_df = con.execute(adjusted_sql).df()
        elapsed_ms = (time.time() - start_time) * 1000.0
        
        columns = list(res_df.columns)
        records = res_df.to_dict(orient="records")
        return columns, records, round(elapsed_ms, 2)
