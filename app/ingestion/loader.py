from pathlib import Path
from typing import List, Tuple

try:
    from pypdf import PdfReader

    HAS_PDF = True
except ImportError:
    HAS_PDF = False


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _read_pdf(path: Path) -> str:
    if not HAS_PDF:
        raise RuntimeError("pypdf is not installed; pip install pypdf to ingest PDFs")
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)


def load_document(path: Path) -> Tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _read_pdf(path), "pdf"
    return _read_text(path), suffix.lstrip(".").lower()


def load_directory(directory: Path, extensions=(".md", ".txt", ".pdf")) -> List[Tuple[str, str, Path]]:
    docs = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions:
            try:
                text, fmt = load_document(path)
                docs.append((text, fmt, path))
            except Exception as exc:
                print(f"[ingest] skip {path.name}: {exc}")
    return docs
