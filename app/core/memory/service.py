import uuid
from typing import Any

from app.core.memory.long_term import LongTermMemoryStore
from app.core.memory.models import MemoryItem, UserPreferences, WorkspacePreferences
from app.core.memory.short_term import ShortTermMemoryCache


class MemoryService:
    def __init__(self) -> None:
        self.short_term = ShortTermMemoryCache()
        self.long_term = LongTermMemoryStore()
        self._session_store: dict[str, dict[str, Any]] = {}
        self._agent_shared_state: dict[str, Any] = {}

    # --- Short-term & Entity Memory ---
    def remember(
        self,
        category: str,
        workspace_id: uuid.UUID,
        key: str,
        value: dict[str, Any],
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
        ttl_seconds: float = 3600.0,
        persist_long_term: bool = True,
    ) -> MemoryItem:
        item = MemoryItem(
            category=category,
            workspace_id=workspace_id,
            user_id=user_id,
            session_id=session_id,
            key=key,
            value=value,
            ttl_seconds=ttl_seconds,
        )
        self.short_term.set(item)
        if persist_long_term:
            self.long_term.save(item)
        return item

    def recall(self, key: str) -> MemoryItem | None:
        item = self.short_term.get(key)
        if not item:
            item = self.long_term.get(key)
        return item

    def recall_recent(self, category: str, workspace_id: uuid.UUID) -> list[dict[str, Any]]:
        items = self.short_term.list_by_category(category, workspace_id)
        return [i.value for i in items]

    # --- Specific Entity Helpers ---
    def add_recent_dataset(self, workspace_id: uuid.UUID, dataset_id: uuid.UUID, metadata: dict[str, Any]) -> MemoryItem:
        key = f"ws:{workspace_id}:dataset:{dataset_id}"
        return self.remember("dataset", workspace_id, key, metadata)

    def add_recent_sql(self, workspace_id: uuid.UUID, sql: str, metadata: dict[str, Any]) -> MemoryItem:
        key = f"ws:{workspace_id}:sql:{uuid.uuid4().hex[:8]}"
        val = {"sql": sql, **metadata}
        return self.remember("sql", workspace_id, key, val)

    def add_previous_dashboard(self, workspace_id: uuid.UUID, dashboard_id: uuid.UUID, spec: dict[str, Any]) -> MemoryItem:
        key = f"ws:{workspace_id}:dashboard:{dashboard_id}"
        return self.remember("dashboard", workspace_id, key, spec)

    def add_previous_report(self, workspace_id: uuid.UUID, report_id: uuid.UUID, report_data: dict[str, Any]) -> MemoryItem:
        key = f"ws:{workspace_id}:report:{report_id}"
        return self.remember("report", workspace_id, key, report_data)

    def add_previous_insight(self, workspace_id: uuid.UUID, insight_id: uuid.UUID, insight_data: dict[str, Any]) -> MemoryItem:
        key = f"ws:{workspace_id}:insight:{insight_id}"
        return self.remember("insight", workspace_id, key, insight_data)

    def add_previous_chat(self, workspace_id: uuid.UUID, session_id: uuid.UUID, message_data: dict[str, Any]) -> MemoryItem:
        key = f"ws:{workspace_id}:chat:{session_id}:{uuid.uuid4().hex[:6]}"
        return self.remember("chat", workspace_id, key, message_data, session_id=str(session_id))

    # --- Preferences ---
    def get_user_preferences(self, user_id: uuid.UUID) -> UserPreferences:
        return self.long_term.get_user_preferences(user_id)

    def set_user_preferences(self, prefs: UserPreferences) -> None:
        self.long_term.set_user_preferences(prefs)

    def get_workspace_preferences(self, workspace_id: uuid.UUID) -> WorkspacePreferences:
        return self.long_term.get_workspace_preferences(workspace_id)

    def set_workspace_preferences(self, prefs: WorkspacePreferences) -> None:
        self.long_term.set_workspace_preferences(prefs)

    # --- Session Memory ---
    @property
    def session_memory(self) -> dict[str, Any]:
        return self._session_store

    def record_chat(self, session_id: str, message: str) -> None:
        if session_id not in self._session_store:
            self._session_store[session_id] = {}
        self._session_store[session_id]["last_chat"] = message

    def set_session_data(self, session_id: str, key: str, value: Any) -> None:
        if session_id not in self._session_store:
            self._session_store[session_id] = {}
        self._session_store[session_id][key] = value

    def get_session_data(self, session_id: str, key: str) -> Any | None:
        return self._session_store.get(session_id, {}).get(key)

    # --- Agent Memory (Shared State) ---
    def set_agent_state(self, agent_name: str, key: str, value: Any) -> None:
        k = f"{agent_name}:{key}"
        self._agent_shared_state[k] = value

    def get_agent_state(self, agent_name: str, key: str) -> Any | None:
        k = f"{agent_name}:{key}"
        return self._agent_shared_state.get(k)

    def cleanup(self) -> int:
        return self.short_term.cleanup_expired()


# Global Memory Service Singleton
global_memory_service = MemoryService()
