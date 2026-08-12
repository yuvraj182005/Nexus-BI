import pytest
from app.search.schemas import GlobalSearchRequest, SavedSearchCreateRequest
from app.search.service import global_search_service


def test_global_search_ranking_and_facets():
    req = GlobalSearchRequest(query="Revenue", use_semantic=True)
    res = global_search_service.search(req)
    assert res.total_matches >= 2
    assert "dataset" in res.facets or "dashboard" in res.facets
    assert len(res.recommendations) >= 1


def test_saved_searches_and_history():
    saved = global_search_service.save_search(SavedSearchCreateRequest(name="Q2 Sales", query="Revenue Q2"))
    assert saved["name"] == "Q2 Sales"

    history = global_search_service.get_search_history()
    assert len(history) >= 1
