from typing import Any

from pydantic import BaseModel


class TextChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    source_type: str  # dataset_meta, glossary, report, insight, doc, chat


class DocumentChunker:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50, metadata: dict[str, Any] | None = None, source_type: str = "doc") -> list[TextChunk]:
        words = text.split()
        chunks = []
        i = 0
        idx = 0
        while i < len(words):
            chunk_words = words[i : i + chunk_size]
            chunk_str = " ".join(chunk_words)
            chunks.append(
                TextChunk(
                    chunk_id=f"chunk_{idx}",
                    text=chunk_str,
                    metadata=metadata or {},
                    source_type=source_type,
                )
            )
            i += chunk_size - overlap
            idx += 1
        return chunks
