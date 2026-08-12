import asyncio
import time

import pandas as pd

from app.connectors.base import (
    ConnectorAdapter,
    ConnectorColumn,
    ConnectorContext,
    ConnectorError,
    ConnectorHealth,
    ConnectorTable,
    ensure_path,
)


class PandasFileAdapter(ConnectorAdapter):
    file_type: str

    def _read(self, context: ConnectorContext) -> pd.DataFrame:
        path = ensure_path(context.config)
        if self.file_type == "csv":
            return pd.read_csv(path)
        if self.file_type == "excel":
            return pd.read_excel(path)
        if self.file_type == "json":
            return pd.json_normalize(pd.read_json(path).to_dict(orient="records"))
        if self.file_type == "parquet":
            return pd.read_parquet(path)
        raise ConnectorError(f"Unsupported file connector: {self.file_type}")

    async def validate(self, context: ConnectorContext) -> ConnectorHealth:
        started = time.perf_counter()
        try:
            frame = await asyncio.to_thread(self._read, context)
        except (OSError, ValueError, TypeError) as exc:
            raise ConnectorError(f"Unable to read {self.file_type} file: {exc}") from exc
        elapsed = (time.perf_counter() - started) * 1000
        return ConnectorHealth(True, f"Read {len(frame)} rows", elapsed)

    async def discover_schema(self, context: ConnectorContext) -> list[ConnectorTable]:
        frame = await asyncio.to_thread(self._read, context)
        columns = [
            ConnectorColumn(
                name=str(column),
                data_type=str(frame[column].dtype),
                nullable=bool(frame[column].isna().any()),
                cardinality=int(frame[column].nunique(dropna=True)),
            )
            for column in frame.columns
        ]
        return [ConnectorTable("data", columns, len(frame))]


class CsvAdapter(PandasFileAdapter):
    file_type = "csv"


class ExcelAdapter(PandasFileAdapter):
    file_type = "excel"


class JsonAdapter(PandasFileAdapter):
    file_type = "json"


class ParquetAdapter(PandasFileAdapter):
    file_type = "parquet"
