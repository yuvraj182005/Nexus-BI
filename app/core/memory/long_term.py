import uuid

from app.core.memory.models import MemoryItem, UserPreferences, WorkspacePreferences


class LongTermMemoryStore:
    def __init__(self) -> None:
        self._persistent_store: dict[str, MemoryItem] = {}
        self._user_prefs: dict[str, UserPreferences] = {}
        self._workspace_prefs: dict[str, WorkspacePreferences] = {}

    def save(self, item: MemoryItem) -> None:
        self._persistent_store[item.key] = item

    def get(self, key: str) -> MemoryItem | None:
        return self._persistent_store.get(key)

    def get_user_preferences(self, user_id: uuid.UUID) -> UserPreferences:
        uid = str(user_id)
        if uid not in self._user_prefs:
            self._user_prefs[uid] = UserPreferences(user_id=user_id)
        return self._user_prefs[uid]

    def set_user_preferences(self, prefs: UserPreferences) -> None:
        self._user_prefs[str(prefs.user_id)] = prefs

    def get_workspace_preferences(self, workspace_id: uuid.UUID) -> WorkspacePreferences:
        wid = str(workspace_id)
        if wid not in self._workspace_prefs:
            self._workspace_prefs[wid] = WorkspacePreferences(workspace_id=workspace_id)
        return self._workspace_prefs[wid]

    def set_workspace_preferences(self, prefs: WorkspacePreferences) -> None:
        self._workspace_prefs[str(prefs.workspace_id)] = prefs
