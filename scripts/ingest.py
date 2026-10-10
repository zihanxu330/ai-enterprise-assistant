import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import BASE_DIR, SAMPLE_DIR
from app.ingestion.chunker import chunk_document
from app.ingestion.loader import load_directory
from app.retrieval.store import VectorStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into the vector store")
    parser.add_argument("--source", default=str(SAMPLE_DIR), help="Directory or file to ingest")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_absolute():
        source = BASE_DIR / source

    store = VectorStore()
    docs = load_directory(source)
    total = 0
    for text, fmt, path in docs:
        chunks = chunk_document(text, str(path))
        store.add(chunks)
        total += len(chunks)
        print(f"[ingest] {path.name} ({fmt}) -> {len(chunks)} chunks")
    print(f"[ingest] done: {len(docs)} documents, {total} chunks")

    query = input("\nTry a question (or press Enter to quit): ").strip()
    while query:
        for score, chunk in store.search(query, top_k=3):
            print(f"  {score:.3f} | {chunk['id']} | {chunk['text'][:120]}")
        query = input("\nNext question (or Enter to quit): ").strip()


if __name__ == "__main__":
    main()
