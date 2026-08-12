from collections.abc import Callable

from app.connectors.base import ConnectorAdapter, ConnectorError
from app.connectors.file_adapters import CsvAdapter, ExcelAdapter, JsonAdapter, ParquetAdapter
from app.connectors.remote_adapters import (
    BigQueryAdapter,
    GoogleSheetsAdapter,
    MongoDbAdapter,
    MySqlAdapter,
    PostgreSqlAdapter,
    RestApiAdapter,
    SnowflakeAdapter,
    SqliteAdapter,
    SqlServerAdapter,
)
from app.models.connector import ConnectorType

ADAPTERS: dict[ConnectorType, Callable[[], ConnectorAdapter]] = {
    ConnectorType.CSV: CsvAdapter,
    ConnectorType.EXCEL: ExcelAdapter,
    ConnectorType.JSON: JsonAdapter,
    ConnectorType.PARQUET: ParquetAdapter,
    ConnectorType.POSTGRESQL: PostgreSqlAdapter,
    ConnectorType.MYSQL: MySqlAdapter,
    ConnectorType.SQL_SERVER: SqlServerAdapter,
    ConnectorType.SQLITE: SqliteAdapter,
    ConnectorType.SNOWFLAKE: SnowflakeAdapter,
    ConnectorType.BIGQUERY: BigQueryAdapter,
    ConnectorType.MONGODB: MongoDbAdapter,
    ConnectorType.GOOGLE_SHEETS: GoogleSheetsAdapter,
    ConnectorType.REST_API: RestApiAdapter,
}


def get_adapter(connector_type: str) -> ConnectorAdapter:
    try:
        return ADAPTERS[ConnectorType(connector_type)]()
    except (KeyError, ValueError) as exc:
        raise ConnectorError(f"Unsupported connector type: {connector_type}") from exc
