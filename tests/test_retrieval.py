import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ingestion.chunker import chunk_document
from app.retrieval.store import VectorStore


def _build_store():
    store = VectorStore()
    chunks = [
        {"id": "faq::chunk-0", "source": "faq", "text": "The dispatch platform uses an LLM engine to balance distance, rating and skill."},
        {"id": "faq::chunk-1", "source": "faq", "text": "API keys are injected via environment variables and git-ignored."},
        {"id": "handbook::chunk-0", "source": "handbook", "text": "Employees receive 12 days of annual leave and 5 sick days."},
    ]
    store.add(chunks)
    return store


def test_search_returns_top_k():
    store = _build_store()
    results = store.search("how does dispatch engine work", top_k=2)
    assert len(results) == 2
    top_id = results[0][1]["id"]
    assert top_id == "faq::chunk-0"


def test_search_empty_store():
    store = VectorStore()
    assert store.search("anything") == []


def test_keyword_and_vector_mix():
    store = _build_store()
    results = store.search("annual leave days", top_k=1)
    assert results[0][1]["id"] == "handbook::chunk-0"
