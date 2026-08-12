from typing import Any

from app.rag.chunking import DocumentChunker, TextChunk
from app.rag.embedding import EmbeddingService
from app.rag.retriever import HybridRetriever


class RAGService:
    def __init__(self, similarity_threshold: float = 0.1) -> None:
        self.embedding_service = EmbeddingService()
        self.retriever = HybridRetriever(self.embedding_service, similarity_threshold=similarity_threshold)
        self._seed_default_knowledge()

    def _seed_default_knowledge(self) -> None:
        # Index Dataset Metadata, Glossary, Reports, Insights, Docs, Chats
        knowledge = [
            ("Dataset Metadata", "SalesDataset contains revenue, customer_id, product_sku, transaction_date.", "dataset_meta"),
            ("Business Glossary", "Revenue: Total monetary value derived from goods sold. Synonym: Turnover.", "glossary"),
            ("Reports", "Q2 Executive Report indicates 14.2% margin expansion in Category A products.", "report"),
            ("Insights", "Anomaly detected in customer churn rate during promotional campaign.", "insight"),
            ("Documentation", "NexusBI AI uses DuckDB for fast in-memory analytics over parquet files.", "doc"),
            ("Previous Chats", "User asked about monthly sales targets and regional growth forecasts.", "chat"),
        ]
        for title, text, src_type in knowledge:
            chunks = DocumentChunker.chunk_text(text, metadata={"title": title}, source_type=src_type)
            for c in chunks:
                self.retriever.index_chunk(c)

    def retrieve(self, query: str, top_k: int = 5) -> tuple[str, list[dict[str, Any]]]:
        top_chunks, citations = self.retriever.hybrid_search(query, top_k=top_k)
        context_snippets = [f"[{c.source_type.upper()}] {c.text}" for c in top_chunks]
        context_text = "\n".join(context_snippets) if context_snippets else "No relevant context found."
        return context_text, citations

    @staticmethod
    def retrieve_context(query: str, dataset_metadata: dict[str, Any] | None = None, top_k: int = 5) -> tuple[str, list[dict[str, Any]]]:
        instance = RAGService()
        if dataset_metadata:
            ds_name = dataset_metadata.get("name", "dataset")
            cols_str = ", ".join(dataset_metadata.get("columns", [])) if isinstance(dataset_metadata.get("columns"), list) else str(dataset_metadata.get("columns"))
            instance.retriever.index_chunk(
                TextChunk(
                    chunk_id="ds_meta_dynamic",
                    text=f"Dataset {ds_name} revenue total schema columns: {cols_str}",
                    metadata=dataset_metadata,
                    source_type="dataset_meta",
                )
            )
        return instance.retrieve(query, top_k=top_k)
