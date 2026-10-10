import time
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import BASE_DIR, TOP_K
from app.eval.metrics import citation_coverage, keyword_grounding, retrieval_hit_rate
from app.ingestion.chunker import chunk_document
from app.ingestion.loader import load_directory
from app.llm.client import LLMClient
from app.llm.prompts import build_prompt
from app.retrieval.store import VectorStore

app = FastAPI(title="AI Enterprise Assistant", version="0.1.0")

store = VectorStore()
llm = LLMClient()


class IngestRequest(BaseModel):
    source: str = Field(default="data/samples", description="Directory or file path to ingest")


class IngestResponse(BaseModel):
    documents: int
    chunks: int


class ChatRequest(BaseModel):
    question: str
    top_k: int = Field(default=TOP_K, ge=1, le=10)


class SourceItem(BaseModel):
    id: str
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    mock: bool
    latency_ms: int


class EvalRequest(BaseModel):
    questions: List[str]
    relevant_ids: Optional[List[List[str]]] = None
    top_k: int = Field(default=4, ge=1, le=10)


class EvalResponse(BaseModel):
    hit_rate: float
    queries: int
    avg_grounding: float


@app.on_event("startup")
def _bootstrap() -> None:
    ingest()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "chunks": len(store.chunks), "mock": llm.mock}


@app.post("/api/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest = None) -> IngestResponse:
    source = Path(req.source) if req else BASE_DIR / "data" / "samples"
    if not source.is_absolute():
        source = BASE_DIR / source
    docs = load_directory(source)
    total = 0
    for text, fmt, path in docs:
        chunks = chunk_document(text, str(path))
        store.add(chunks)
        total += len(chunks)
    return IngestResponse(documents=len(docs), chunks=total)


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    start = time.perf_counter()
    results = store.search(req.question, top_k=req.top_k)
    chunks = [c for _, c in results]
    context = build_prompt(req.question, chunks)
    answer = llm.chat(req.question, context)
    sources = [SourceItem(id=c["id"], text=c["text"], score=round(s, 4)) for s, c in results]
    latency = int((time.perf_counter() - start) * 1000)
    return ChatResponse(answer=answer, sources=sources, mock=llm.mock, latency_ms=latency)


@app.post("/api/evaluate", response_model=EvalResponse)
def evaluate(req: EvalRequest) -> EvalResponse:
    results_by_query = {}
    relevant = {}
    for i, q in enumerate(req.questions):
        results_by_query[q] = store.search(q, top_k=req.top_k)
        if req.relevant_ids and i < len(req.relevant_ids):
            relevant[q] = set(req.relevant_ids[i])
    hit_rate, total = retrieval_hit_rate(results_by_query, relevant)
    grounding_scores = []
    for q, results in results_by_query.items():
        answer = llm.chat(q, build_prompt(q, [c for _, c in results]))
        context = "\n".join(c["text"] for _, c in results)
        grounding_scores.append(keyword_grounding(answer, context))
    avg_grounding = sum(grounding_scores) / len(grounding_scores) if grounding_scores else 0.0
    return EvalResponse(hit_rate=hit_rate, queries=total, avg_grounding=round(avg_grounding, 4))
