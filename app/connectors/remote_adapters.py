import time
from typing import Any

import httpx
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine

from app.connectors.base import (
    ConnectorAdapter,
    ConnectorColumn,
    ConnectorContext,
    ConnectorError,
    ConnectorHealth,
    ConnectorTable,
)


class RestApiAdapter(ConnectorAdapter):
    async def validate(self, context: ConnectorContext) -> ConnectorHealth:
        url = context.config.get("url")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            raise ConnectorError("REST connector requires an HTTP or HTTPS URL")
        headers = context.credentials.get("headers", {})
        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.request(context.config.get("method", "GET"), url, headers=headers)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ConnectorError(f"REST API validation failed: {exc}") from exc
        return ConnectorHealth(True, f"HTTP {response.status_code}", (time.perf_counter() - started) * 1000)

    async def discover_schema(self, context: ConnectorContext) -> list[ConnectorTable]:
        url = context.config.get("url")
        headers = context.credentials.get("headers", {})
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ConnectorError(f"REST schema discovery failed: {exc}") from exc
        records = payload if isinstance(payload, list) else payload.get("data", payload.get("results", []))
        if not isinstance(records, list) or not records:
            return [ConnectorTable("response", [])]
        first = records[0]
        if not isinstance(first, dict):
            raise ConnectorError("REST response must contain JSON objects for schema discovery")
        return [ConnectorTable("response", [self._column(name, value) for name, value in first.items()], len(records))]

    @staticmethod
    def _column(name: str, value: Any):
        return ConnectorColumn(name=name, data_type=type(value).__name__)


class OptionalDependencyAdapter(ConnectorAdapter):
    dependency_name: str
    display_name: str

    async def validate(self, context: ConnectorContext) -> ConnectorHealth:
        raise ConnectorError(
            f"{self.display_name} requires the optional '{self.dependency_name}' connector dependency"
        )

    async def discover_schema(self, context: ConnectorContext) -> list[ConnectorTable]:
        await self.validate(context)
        return []


class SqlAlchemyAdapter(ConnectorAdapter):
    async def validate(self, context: ConnectorContext) -> ConnectorHealth:
        url = self._url(context)
        started = time.perf_counter()
        try:
            engine = create_async_engine(url, pool_pre_ping=True, pool_recycle=1800, pool_timeout=15)
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        except Exception as exc:
            raise ConnectorError(f"Database connection failed: {exc}") from exc
        finally:
            if "engine" in locals():
                await engine.dispose()
        return ConnectorHealth(True, "Database connection succeeded", (time.perf_counter() - started) * 1000)

    async def discover_schema(self, context: ConnectorContext) -> list[ConnectorTable]:
        try:
            engine = create_async_engine(
                self._url(context), pool_pre_ping=True, pool_recycle=1800, pool_timeout=15
            )
            async with engine.connect() as connection:
                tables = await connection.run_sync(self._inspect_tables)
                result: list[ConnectorTable] = []
                for table_name, columns in tables:
                    count = await connection.scalar(text(f'SELECT COUNT(*) FROM "{table_name}"'))
                    result.append(ConnectorTable(table_name, columns, int(count or 0)))
                return result
        except Exception as exc:
            raise ConnectorError(f"Database schema discovery failed: {exc}") from exc
        finally:
            if "engine" in locals():
                await engine.dispose()

    @staticmethod
    def _url(context: ConnectorContext) -> str:
        url = context.credentials.get("url") or context.config.get("url")
        if not isinstance(url, str) or not url:
            raise ConnectorError("Relational connectors require a SQLAlchemy URL")
        return url

    @staticmethod
    def _inspect_tables(connection) -> list[tuple[str, list[Any]]]:
        inspector = inspect(connection)
        tables = []
        for table_name in inspector.get_table_names():
            columns = [
                ConnectorColumn(
                    name=column["name"],
                    data_type=str(column["type"]),
                    nullable=bool(column.get("nullable", True)),
                )
                for column in inspector.get_columns(table_name)
            ]
            tables.append((table_name, columns))
        return tables


class PostgreSqlAdapter(SqlAlchemyAdapter):
    pass


class MySqlAdapter(SqlAlchemyAdapter):
    pass


class SqlServerAdapter(SqlAlchemyAdapter):
    pass


class SqliteAdapter(SqlAlchemyAdapter):
    pass


class SnowflakeAdapter(OptionalDependencyAdapter):
    dependency_name = "snowflake-connector-python"
    display_name = "Snowflake"


class BigQueryAdapter(OptionalDependencyAdapter):
    dependency_name = "google-cloud-bigquery"
    display_name = "BigQuery"


class MongoDbAdapter(OptionalDependencyAdapter):
    dependency_name = "motor"
    display_name = "MongoDB"


class GoogleSheetsAdapter(OptionalDependencyAdapter):
    dependency_name = "gspread"
    display_name = "Google Sheets"
