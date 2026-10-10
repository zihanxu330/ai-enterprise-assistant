import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ingestion.chunker import chunk_document, split_text


def test_split_small_text():
    text = "Short document."
    assert split_text(text) == ["Short document."]


def test_chunk_document_ids():
    text = "Word " * 200
    chunks = chunk_document(text, "handbook.md")
    assert len(chunks) >= 2
    assert all(c["source"] == "handbook.md" for c in chunks)
    ids = [c["id"] for c in chunks]
    assert len(set(ids)) == len(ids)
    assert ids[0] == "handbook.md::chunk-0"


def test_overlap_present():
    text = "Sentence " * 300
    chunks = chunk_document(text, "doc.txt", chunk_size=400, overlap=80)
    assert len(chunks) > 1
    assert chunks[0]["index"] == 0
    assert chunks[1]["index"] == 1
