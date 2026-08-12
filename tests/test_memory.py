import time
import uuid
import pytest
from app.core.memory import (
    MemoryService,
    UserPreferences,
    WorkspacePreferences,
)


def test_short_term_memory_ttl():
    service = MemoryService()
    ws_id = uuid.uuid4()
    item = service.remember("dataset", ws_id, "test_key", {"name": "Sales"}, ttl_seconds=0.1)

    rec = service.recall("test_key")
    assert rec is not None
    assert rec.value["name"] == "Sales"

    time.sleep(0.15)
    expired_rec = service.short_term.get("test_key")
    assert expired_rec is None


def test_entity_helpers():
    service = MemoryService()
    ws_id = uuid.uuid4()
    ds_id = uuid.uuid4()

    service.add_recent_dataset(ws_id, ds_id, {"title": "Q3 Financials"})
    recent_datasets = service.recall_recent("dataset", ws_id)
    assert len(recent_datasets) == 1
    assert recent_datasets[0]["title"] == "Q3 Financials"


def test_preferences_memory():
    service = MemoryService()
    user_id = uuid.uuid4()
    ws_id = uuid.uuid4()

    u_prefs = service.get_user_preferences(user_id)
    assert u_prefs.preferred_dialect == "duckdb"

    u_prefs.preferred_theme = "light"
    service.set_user_preferences(u_prefs)

    updated = service.get_user_preferences(user_id)
    assert updated.preferred_theme == "light"

    ws_prefs = service.get_workspace_preferences(ws_id)
    assert ws_prefs.default_ai_provider == "openai"


def test_agent_and_session_memory():
    service = MemoryService()
    service.set_session_data("session_123", "last_intent", "sql_query")
    assert service.get_session_data("session_123", "last_intent") == "sql_query"

    service.set_agent_state("SQLAgent", "last_table", "revenue_table")
    assert service.get_agent_state("SQLAgent", "last_table") == "revenue_table"
