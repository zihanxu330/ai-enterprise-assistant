# AI Enterprise Assistant

An **LLM-powered enterprise knowledge assistant** built with Retrieval-Augmented Generation (RAG): feed it your internal documents, and it answers questions grounded in that knowledge base — with source citations, so answers are verifiable instead of hallucinated.

**Working pipeline, out of the box:** document ingestion → chunking → TF-IDF vector indexing → hybrid retrieval → grounded Q&A with citations → basic evaluation. No LLM API key is required to run the full pipeline (mock mode), and swapping in a real LLM is a one-line `.env` change.

---

## ✨ Features

- **Enterprise knowledge base**: ingest `.md` / `.txt` / `.pdf` documents (recursive directory scan)
- **RAG retrieval**: TF-IDF vector similarity blended with keyword overlap (hybrid), top-k chunk selection
- **Grounded Q&A**: LLM answers with source chunk citations (`[id]` format), system prompt enforces "answer only from context"
- **Mock mode**: without an API key, a deterministic mock answer runs the entire chain — perfect for CI and demos
- **Evaluation**: retrieval hit-rate + answer grounding metrics via `/api/evaluate`
- **REST API**: FastAPI with `/api/ingest`, `/api/chat`, `/api/evaluate`, `/health`

---

## 🏗 Tech Stack

| Layer | Technology |
| --- | --- |
| API Framework | FastAPI + Uvicorn |
| Retrieval | Python TF-IDF + cosine similarity + keyword overlap (numpy) |
| LLM | DeepSeek / OpenAI-compatible chat API (`deepseek-chat`) |
| Document Parsing | pypdf (PDF) + plain text / Markdown |
| Evaluation | Custom metrics (hit-rate, grounding) |

## 🧱 Architecture

```
Enterprise documents (.md / .txt / .pdf)
        │  /api/ingest (loader + chunker)
        ▼
Chunking (500 chars, 80 overlap) ──► TF-IDF vector index
                                              │
User question ──► /api/chat ──► hybrid retrieval (vector 0.7 + keyword 0.3)
                                              │
                                              ▼
                              Context assembly (top-k chunks, cited)
                                              │
                                              ▼
                              LLM answer generation (or mock mode)
                                              │
                                              ▼
                          Response: answer + sources + latency
```

## 📁 Project Structure

```
ai-enterprise-assistant/
├── app/
│   ├── main.py             # FastAPI entry: ingest / chat / evaluate / health
│   ├── config.py           # .env config (LLM keys, chunk size, top-k)
│   ├── ingestion/
│   │   ├── loader.py       # document loading (.md / .txt / .pdf)
│   │   └── chunker.py      # overlapping text chunking
│   ├── retrieval/
│   │   ├── embeddings.py   # tokenizer, TF-IDF, cosine, keyword overlap
│   │   └── store.py        # in-memory vector store + hybrid search
│   ├── llm/
│   │   ├── client.py       # DeepSeek / OpenAI-compatible client + mock mode
│   │   └── prompts.py      # system prompt + QA template + context builder
│   └── eval/
│       └── metrics.py      # retrieval hit-rate, citation coverage, grounding
├── data/
│   └── samples/            # sample enterprise docs (handbook + product FAQ)
├── scripts/
│   └── ingest.py           # CLI: ingest documents + interactive search
├── tests/                  # pytest: ingestion + retrieval unit tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # optional: add LLM_API_KEY for real answers
```

### 2. Run the API server

```bash
uvicorn app.main:app --reload
```

The server auto-ingests `data/samples` on startup.

### 3. Try it

**Health check** (GET):
```bash
curl http://127.0.0.1:8000/health
# {"status":"ok","chunks":8,"mock":true}
```

**Chat** (POST):
```bash
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" \
  -d '{"question":"How many days of annual leave do employees get?","top_k":3}'
```

**Ingest your own documents** (POST):
```bash
curl -X POST http://127.0.0.1:8000/api/ingest -H "Content-Type: application/json" \
  -d '{"source":"/absolute/path/to/your/docs"}'
```

**Evaluate** (POST):
```bash
curl -X POST http://127.0.0.1:8000/api/evaluate -H "Content-Type: application/json" \
  -d '{"questions":["How does order dispatch work?"],"top_k":3}'
```

### 4. CLI mode (no server)

```bash
python scripts/ingest.py --source data/samples
```

---

## 🔑 Enable real LLM answers

Edit `.env`:

```bash
LLM_API_KEY=your_deepseek_or_openai_key
LLM_BASE_URL=https://api.deepseek.com   # or any OpenAI-compatible endpoint
LLM_MODEL=deepseek-chat
```

Without a key, the API runs in **mock mode** (`"mock": true`) — the whole RAG chain still works, useful for CI, demos and development.

## 📈 Evaluation

`/api/evaluate` measures:

- **Retrieval hit-rate**: does the retrieved top-k set contain the expected relevant chunks?
- **Answer grounding**: what fraction of answer tokens appears in the retrieved context?

Extend `app/eval/metrics.py` with RAGAS-style metrics (faithfulness, answer relevance, retrieval precision) as the project grows.

---

## 🗺 Roadmap

- [x] Ingestion: MD / TXT / PDF chunking pipeline
- [x] Vector store: TF-IDF index + hybrid retrieval
- [x] Chat API: grounded Q&A with citations (mock mode included)
- [x] Prompt templates + system prompt
- [x] Basic evaluation endpoint
- [ ] OpenAI / other embedding models (replace TF-IDF)
- [ ] Persistent vector DB (Chroma / FAISS)
- [ ] Multi-turn conversation memory
- [ ] RAGAS-style faithfulness & relevance metrics
- [ ] Docker + CI pipeline

## 🔒 Security Notes

- API keys injected via environment variables only; `.env` is git-ignored
- Sample documents are fictional; add RBAC for knowledge-base access in enterprise deployment

## 📄 License

[MIT](LICENSE)
