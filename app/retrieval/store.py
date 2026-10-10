from typing import Dict, List, Tuple

from app.retrieval.embeddings import TfidfVectorizer, cosine, keyword_overlap


class VectorStore:
    def __init__(self) -> None:
        self.chunks: List[dict] = []
        self.vectors: List[Dict[str, float]] = []
        self.vectorizer = TfidfVectorizer()

    def add(self, chunks: List[dict]) -> int:
        if not chunks:
            return 0
        corpus = [c["text"] for c in chunks]
        if not self.vectors:
            self.vectorizer.fit(corpus)
        else:
            self.vectorizer.fit([c["text"] for c in self.chunks] + corpus)
            self.vectors = [self.vectorizer.transform(c["text"]) for c in self.chunks]
        new_vectors = [self.vectorizer.transform(c["text"]) for c in chunks]
        self.chunks.extend(chunks)
        self.vectors.extend(new_vectors)
        return len(chunks)

    def search(self, query: str, top_k: int = 4, alpha: float = 0.7) -> List[Tuple[float, dict]]:
        if not self.chunks:
            return []
        qv = self.vectorizer.transform(query)
        scored = []
        for vec, chunk in zip(self.vectors, self.chunks):
            vec_score = cosine(qv, vec)
            kw_score = keyword_overlap(query, chunk["text"])
            blended = alpha * vec_score + (1 - alpha) * kw_score
            scored.append((blended, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]
