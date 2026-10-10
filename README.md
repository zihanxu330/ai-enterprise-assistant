# AI Enterprise Assistant

> **Status: in development** — architecture & scaffold planned, implementation in progress.

An **LLM-powered enterprise knowledge assistant** built with Retrieval-Augmented Generation (RAG): an enterprise feeds in its internal documents, and the assistant answers questions grounded in that knowledge base — with citations, so answers are verifiable instead of hallucinated.

Designed to sit inside a company workflow: employees ask in natural language, the system retrieves the most relevant chunks from a vector database, and the LLM composes an answer with sources attached.

---

## 🎯 Goals

- **Enterprise knowledge base**: ingest PDFs / Markdown / HTML into a searchable index
- **RAG retrieval**: hybrid retrieval (vector + keyword) over internal documents
- **Grounded Q&A**: LLM answers with source citations, reducing hallucination
- **Prompt optimization**: structured system prompts + few-shot templates
- **Conversation management**: multi-turn dialogue with memory of context

---

## 🏗 Planned Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python |
| API Framework | FastAPI |
| LLM | DeepSeek / OpenAI-compatible chat API |
| Vector Database | Chroma / FAISS |
| Document Parsing | PDF / Markdown ingestion pipeline |
| Evaluation | RAGAS / LLM-as-judge (answer grounding & retrieval quality) |

## 🧱 Planned Architecture

```
Enterprise documents
        │  ingestion pipeline
        ▼
Chunking + embedding ──► Vector Database
                              │
User question ──► Query router │
                     │        ▼
                     ├──► Hybrid retrieval (vector + keyword)
                     │        ▼
                     ├──► Context assembly (top-k chunks)
                     │        ▼
                     └──► LLM answer generation + citations
                              │
                              ▼
                     FastAPI /api/chat + /api/evaluate
```

## 📁 Planned Structure

```
ai-enterprise-assistant/
├── app/
│   ├── main.py             # FastAPI entry
│   ├── ingestion/          # document parsing + chunking + embedding
│   ├── retrieval/          # vector store + hybrid search
│   ├── llm/                # prompt templates + chat completion
│   └── eval/               # retrieval & answer quality evaluation
├── data/                   # sample documents (git-ignored except samples)
├── tests/
├── requirements.txt
├── .env.example            # API keys (never commit real keys)
└── README.md
```

---

## 🚀 Quick Start (planned)

```bash
pip install -r requirements.txt
cp .env.example .env        # fill in LLM API key
python -m app.ingestion.run --source data/samples
uvicorn app.main:app --reload
```

---

## 🗺 Roadmap

- [ ] Ingestion: PDF / Markdown chunking pipeline
- [ ] Vector store: embed + index + hybrid retrieval
- [ ] Chat API: grounded Q&A with citations
- [ ] Prompt optimization & few-shot templates
- [ ] Evaluation: RAGAS-style metrics (faithfulness, answer relevance, retrieval precision)
- [ ] Multi-turn conversation memory

## 🔒 Security Notes

- API keys injected via environment variables only; `.env` git-ignored
- Optionally add RBAC for knowledge-base access in enterprise deployment

## 📄 License

[MIT](LICENSE)
