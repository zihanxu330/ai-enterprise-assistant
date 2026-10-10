from typing import Dict, List, Tuple

from app.retrieval.embeddings import tokenize


def retrieval_hit_rate(results_by_query: Dict[str, List], relevant_ids_by_query: Dict[str, set], k: int = 4) -> Tuple[float, int]:
    hits = 0
    total = 0
    for q, results in results_by_query.items():
        if q not in relevant_ids_by_query:
            continue
        total += 1
        retrieved = {c["id"] for _, c in results[:k]}
        if retrieved & relevant_ids_by_query[q]:
            hits += 1
    rate = hits / total if total else 0.0
    return rate, total


def citation_coverage(answer: str, chunk_ids: List[str]) -> float:
    cited = {c.split("::")[0] for c in chunk_ids if c.split("::")[0] in answer}
    return len(cited) / len(chunk_ids) if chunk_ids else 0.0


def keyword_grounding(answer: str, context: str) -> float:
    a = set(tokenize(answer))
    c = set(tokenize(context))
    if not a:
        return 0.0
    return len(a & c) / len(a)
