import time
from typing import Any

from app.core.memory.models import MemoryItem


class ShortTermMemoryCache:
    def __init__(self, max_size: int = 1000) -> None:
        self.max_size = max_size
        self._store: dict[str, MemoryItem] = {}

    def set(self, item: MemoryItem) -> None:
        self.cleanup_expired()
        if len(self._store) >= self.max_size:
            # Evict oldest item (LRU strategy)
            oldest_key = min(self._store.keys(), key=lambda k: self._store[k].created_at)
            del self._store[oldest_key]
        self._store[item.key] = item

    def get(self, key: str) -> MemoryItem | None:
        item = self._store.get(key)
        if not item:
            return None
        if item.is_expired:
            del self._store[key]
            return None
        return item

    def delete(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    def cleanup_expired(self) -> int:
        now = time.time()
        expired_keys = [k for k, v in self._store.items() if now > (v.created_at + v.ttl_seconds)]
        for k in expired_keys:
            del self._store[k]
        return len(expired_keys)

    def list_by_category(self, category: str, workspace_id: Any) -> list[MemoryItem]:
        self.cleanup_expired()
        return [
            v for v in self._store.values()
            if v.category == category and str(v.workspace_id) == str(workspace_id)
        ]
