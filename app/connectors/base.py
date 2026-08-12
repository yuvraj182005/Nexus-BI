from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ConnectorColumn:
    name: str
    data_type: str
    nullable: bool = True
    cardinality: int | None = None


@dataclass(frozen=True)
class ConnectorTable:
    name: str
    columns: list[ConnectorColumn]
    row_count: int | None = None


@dataclass(frozen=True)
class ConnectorHealth:
    healthy: bool
    message: str
    latency_ms: float | None = None


@dataclass
class ConnectorContext:
    config: dict[str, Any]
    credentials: dict[str, Any]


class ConnectorError(Exception):
    """Expected adapter failure with a user-safe message."""


class ConnectorAdapter(ABC):
    @abstractmethod
    async def validate(self, context: ConnectorContext) -> ConnectorHealth:
        raise NotImplementedError

    @abstractmethod
    async def discover_schema(self, context: ConnectorContext) -> list[ConnectorTable]:
        raise NotImplementedError

    async def health_check(self, context: ConnectorContext) -> ConnectorHealth:
        return await self.validate(context)

    async def sync(self, context: ConnectorContext) -> tuple[int, list[ConnectorTable]]:
        tables = await self.discover_schema(context)
        return sum(table.row_count or 0 for table in tables), tables


def ensure_path(config: dict[str, Any]) -> Path:
    path = config.get("path")
    if not isinstance(path, str) or not path:
        raise ConnectorError("A local connector requires a file path")
    file_path = Path(path)
    if not file_path.is_file():
        raise ConnectorError("The configured connector file does not exist")
    return file_path
