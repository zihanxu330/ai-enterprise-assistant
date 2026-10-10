import math
import re
from collections import Counter
from typing import Dict, List, Tuple

TOKEN_RE = re.compile(r"[a-zA-Z\u4e00-\u9fff0-9]+")


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


class TfidfVectorizer:
    def __init__(self) -> None:
        self.idf: Dict[str, float] = {}
        self.fitted = False

    def fit(self, corpus: List[str]) -> "TfidfVectorizer":
        n = len(corpus)
        df: Counter = Counter()
        for doc in corpus:
            for term in set(tokenize(doc)):
                df[term] += 1
        self.idf = {term: math.log((1 + n) / (1 + count)) + 1.0 for term, count in df.items()}
        self.fitted = True
        return self

    def transform(self, text: str) -> Dict[str, float]:
        if not self.fitted:
            raise RuntimeError("TfidfVectorizer.fit must be called before transform")
        counts = Counter(tokenize(text))
        total = sum(counts.values())
        if total == 0:
            return {}
        vec = {}
        for term, count in counts.items():
            if term in self.idf:
                vec[term] = (count / total) * self.idf[term]
        return vec


def cosine(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    common = set(vec_a) & set(vec_b)
    dot = sum(vec_a[t] * vec_b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def keyword_overlap(query: str, doc: str) -> float:
    q_terms = set(tokenize(query))
    d_terms = set(tokenize(doc))
    if not q_terms:
        return 0.0
    return len(q_terms & d_terms) / len(q_terms)
