import hashlib
import json
from typing import Any


class SemanticQueryCache:
    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def _hash(self, key_data: Any) -> str:
        s = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def get(self, key_data: Any) -> Any | None:
        k = self._hash(key_data)
        return self._cache.get(k)

    def set(self, key_data: Any, value: Any) -> None:
        k = self._hash(key_data)
        self._cache[k] = value


global_query_cache = SemanticQueryCache()
