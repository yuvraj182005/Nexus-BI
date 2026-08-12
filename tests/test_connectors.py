from pathlib import Path

import pandas as pd
import pytest

from app.connectors.base import ConnectorContext, ConnectorError
from app.connectors.file_adapters import CsvAdapter
from app.connectors.registry import get_adapter
from app.connectors.security import decrypt_credentials, encrypt_credentials
from app.connectors.remote_adapters import RestApiAdapter, SqliteAdapter
from app.models.connector import ConnectorType


def test_credentials_are_encrypted_and_round_trip() -> None:
    credentials = {"password": "do-not-store-plain", "token": "secret-token"}
    encrypted = encrypt_credentials(credentials)

    assert "do-not-store-plain" not in encrypted
    assert decrypt_credentials(encrypted) == credentials


def test_registry_contains_all_supported_connector_types() -> None:
    for connector_type in ConnectorType:
        assert get_adapter(connector_type.value)


@pytest.mark.asyncio
async def test_csv_adapter_discovers_schema(tmp_path: Path) -> None:
    path = tmp_path / "sales.csv"
    pd.DataFrame({"region": ["west", "east"], "revenue": [100, 200]}).to_csv(path, index=False)

    tables = await CsvAdapter().discover_schema(ConnectorContext({"path": str(path)}, {}))

    assert tables[0].name == "data"
    assert tables[0].row_count == 2
    assert {column.name for column in tables[0].columns} == {"region", "revenue"}


@pytest.mark.asyncio
async def test_sql_adapter_requires_url() -> None:
    with pytest.raises(ConnectorError, match="SQLAlchemy URL"):
        await SqliteAdapter().validate(ConnectorContext({}, {}))


def test_rest_adapter_is_registered() -> None:
    assert isinstance(get_adapter(ConnectorType.REST_API.value), RestApiAdapter)
