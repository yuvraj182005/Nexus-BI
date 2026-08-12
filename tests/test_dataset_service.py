from pathlib import Path

import pytest

from app.services.dataset import DatasetService
from app.storage.local import LocalObjectStorage


@pytest.mark.parametrize(
    ("filename", "expected"),
    [("sales.csv", "csv"), ("sales.xlsx", "xlsx"), ("sales.json", "json"), ("sales.parquet", "parquet")],
)
def test_supported_dataset_formats(filename: str, expected: str) -> None:
    assert DatasetService._format(filename) == expected


def test_unsupported_dataset_format_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported dataset format"):
        DatasetService._format("sales.exe")


def test_dataset_slug_is_stable_and_bounded() -> None:
    assert DatasetService._slug(" Revenue 2026 ") == "revenue-2026"


def test_local_storage_rejects_path_traversal(tmp_path: Path) -> None:
    storage = LocalObjectStorage(str(tmp_path))

    with pytest.raises(ValueError, match="Invalid storage key"):
        storage.path_for("../../outside.csv")
