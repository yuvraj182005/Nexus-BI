import re
from typing import Any

from app.rag.chunking import TextChunk
from app.rag.embedding import EmbeddingService


class HybridRetriever:
    def __init__(self, embedding_service: EmbeddingService | None = None, similarity_threshold: float = 0.1) -> None:
        self.embedding_service = embedding_service or EmbeddingService()
        self.similarity_threshold = similarity_threshold
        self._vector_db: list[tuple[TextChunk, list[float]]] = []

    def index_chunk(self, chunk: TextChunk) -> None:
        vec = self.embedding_service.embed_text(chunk.text)
        self._vector_db.append((chunk, vec))

    def hybrid_search(self, query: str, top_k: int = 5) -> tuple[list[TextChunk], list[dict[str, Any]]]:
        query_vec = self.embedding_service.embed_text(query)
        raw_words = set(re.findall(r"\w+", query.lower()))
        stopwords = {"what", "is", "a", "an", "the", "for", "to", "in", "of", "and", "or", "how", "why"}
        query_words = raw_words - stopwords or raw_words

        scored_results: list[tuple[TextChunk, float]] = []

        for chunk, chunk_vec in self._vector_db:
            # Semantic score
            sem_score = self.embedding_service.cosine_similarity(query_vec, chunk_vec)
            # Keyword score (BM25 surrogate)
            chunk_words = set(re.findall(r"\w+", chunk.text.lower()))
            overlap = len(query_words.intersection(chunk_words))
            kw_score = overlap / len(query_words) if query_words else 0.0

            # Hybrid Score (60% semantic + 40% keyword)
            hybrid_score = (0.6 * sem_score) + (0.4 * kw_score)

            if hybrid_score >= self.similarity_threshold:
                scored_results.append((chunk, hybrid_score))

        # Re-ranking & Context Ranking
        scored_results.sort(key=lambda x: x[1], reverse=True)

        top_chunks = [item[0] for item in scored_results[:top_k]]
        citations = []
        for chunk, score in scored_results[:top_k]:
            citations.append({
                "chunk_id": chunk.chunk_id,
                "source": chunk.metadata.get("name") or chunk.metadata.get("title") or chunk.source_type,
                "source_type": chunk.source_type,
                "score": round(score, 4),
                "source_metadata": chunk.metadata,
                "text_snippet": chunk.text[:120] + "...",
            })

        return top_chunks, citations
