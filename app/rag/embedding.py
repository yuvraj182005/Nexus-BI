import hashlib
import math


class EmbeddingCache:
    def __init__(self) -> None:
        self._cache: dict[str, list[float]] = {}

    def get(self, text: str) -> list[float] | None:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return self._cache.get(h)

    def set(self, text: str, embedding: list[float]) -> None:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        self._cache[h] = embedding


class EmbeddingService:
    def __init__(self, dimension: int = 1536) -> None:
        self.dimension = dimension
        self.cache = EmbeddingCache()

    def embed_text(self, text: str) -> list[float]:
        cached = self.cache.get(text)
        if cached:
            return cached

        # Deterministic pseudo-embedding for testing/local execution
        h = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
        vec = [(float((h >> (i % 32)) & 0xFF) / 255.0) - 0.5 for i in range(self.dimension)]
        # Normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        normalized = [x / norm for x in vec]
        self.cache.set(text, normalized)
        return normalized

    @staticmethod
    def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
        if len(vec1) != len(vec2):
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        n1 = math.sqrt(sum(a * a for a in vec1))
        n2 = math.sqrt(sum(b * b for b in vec2))
        return dot / (n1 * n2) if (n1 * n2) > 0 else 0.0
