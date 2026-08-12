import pytest
from app.rag.service import RAGService


def test_rag_retrieval():
    context, citations = RAGService.retrieve_context("What is total revenue?", {"name": "SalesData", "columns": ["revenue", "date"]})
    assert "SalesData" in context
    assert len(citations) >= 1
    assert citations[0]["source"] == "SalesData"
