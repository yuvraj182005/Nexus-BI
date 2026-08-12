import pytest
from app.rag.chunking import DocumentChunker
from app.rag.embedding import EmbeddingService
from app.rag.retriever import HybridRetriever
from app.rag.service import RAGService


def test_embedding_cache_and_similarity():
    service = EmbeddingService(dimension=64)
    v1 = service.embed_text("revenue growth")
    v2 = service.embed_text("revenue growth")
    v3 = service.embed_text("unrelated random text")

    assert len(v1) == 64
    assert v1 == v2  # Cache hit
    sim_same = EmbeddingService.cosine_similarity(v1, v2)
    assert abs(sim_same - 1.0) < 0.001


def test_document_chunker():
    text = "Word " * 1000
    chunks = DocumentChunker.chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 1
    assert chunks[0].chunk_id == "chunk_0"


def test_hybrid_retrieval_and_citations():
    service = RAGService()
    context, citations = service.retrieve("What is total revenue turnover?")
    assert len(citations) >= 1
    assert "glossary" in [c["source_type"] for c in citations] or "dataset_meta" in [c["source_type"] for c in citations]
