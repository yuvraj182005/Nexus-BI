import uuid
import pytest
from app.catalog.schemas import CatalogSearchRequest


def test_catalog_schemas():
    req = CatalogSearchRequest(query="Sales", starred_only=True)
    assert req.query == "Sales"
    assert req.starred_only is True
