from typing import List
from app.config import CHUNK_OVERLAP, CHUNK_SIZE


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        boundary = text.rfind("\n\n", start + chunk_size // 2, end)
        if boundary == -1:
            boundary = text.rfind(". ", start + chunk_size // 2, end)
        if boundary != -1 and boundary > start:
            end = boundary + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(start, end - overlap)

    return chunks


def chunk_document(text: str, source: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[dict]:
    pieces = split_text(text, chunk_size, overlap)
    return [
        {"id": f"{source}::chunk-{i}", "source": source, "text": piece, "index": i}
        for i, piece in enumerate(pieces)
    ]
