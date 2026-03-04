# Document Intelligence — AI/ML POC for Environmental & Social Use Cases

A **Proof of Concept** application that demonstrates **RAG** (Retrieval-Augmented Generation), **vector search**, **REST APIs**, and **MLOps** (MLflow) in a single Python codebase—without Docker. Built to showcase AI engineering skills relevant to document-driven workflows (e.g. environmental and social specialists).

---

## What This POC Demonstrates

| Area | How It's Shown |
|------|----------------|
| **LLMs & RAG** | Natural language Q&A over your documents; optional OpenAI integration for answer generation |
| **Vector databases** | ChromaDB for semantic search over document chunks |
| **NLP / embeddings** | sentence-transformers (local) or OpenAI embeddings; configurable chunking |
| **API management** | FastAPI REST API with OpenAPI docs; health, ingest, and query endpoints |
| **MLOps** | MLflow for experiment tracking (query and ingest runs) |
| **Documentation** | Architecture doc, user guide, and inline specs |
| **Ethics & governance** | Local-first option, configurable retention, no training on your data |

---

## Quick Start

### Prerequisites
- **Python 3.10+**
- No Docker required; everything runs in-process.

### 1. Clone / open project and install dependencies
```bash
cd WB_POC
pip install -r requirements.txt
```

### 2. Start the API server
```bash
python run_api.py
```
- API: **http://127.0.0.1:8000**
- Interactive docs: **http://127.0.0.1:8000/docs**

### 3. (Optional) Start the web UI
In a **second terminal**:
```bash
python run_ui.py
```
- UI: **http://localhost:8501**

### 4. Ingest sample documents and ask questions
- **Sample files** are in `sample_docs/` (environmental and social safeguard excerpts).
- **Via UI:** Use the "Ingest documents" tab to upload them, then "Ask a question" (e.g. *"What are the main environmental risks?"*).
- **Via API:** `POST /api/v1/ingest` with multipart files, then `POST /api/v1/query` with `{"question": "..."}`.

---

## Project Structure

```
WB_POC/
├── README.md                 # This file
├── ARCHITECTURE.md           # System design and data flow
├── requirements.txt
├── .env.example
├── config/
│   └── settings.py           # Centralized configuration
├── app/
│   ├── main.py               # FastAPI app
│   ├── api/
│   │   ├── routes.py         # REST endpoints
│   │   └── schemas.py        # Pydantic models
│   ├── core/
│   │   ├── embeddings.py     # Local / OpenAI embeddings
│   │   ├── vector_store.py   # ChromaDB wrapper
│   │   └── rag.py            # RAG pipeline
│   └── services/
│       └── document_processor.py  # PDF/TXT chunking
├── docs/
│   └── USER_GUIDE.md
├── sample_docs/              # Example environmental/social text
├── mlflow_utils.py           # MLflow logging helpers
├── run_api.py                # Start FastAPI server
├── run_ui.py                 # Start Streamlit UI
└── streamlit_app.py          # Streamlit front-end
```

---

## Configuration

Copy `.env.example` to `.env` and adjust as needed:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Optional. Enables OpenAI embeddings and/or LLM for answers. |
| `CHROMA_PERSIST_DIR` | Where ChromaDB stores vectors (default: `./data/chroma`). |
| `MLFLOW_TRACKING_URI` | Where MLflow stores runs (default: `./mlruns`). |

Without `OPENAI_API_KEY`, the app uses **local** sentence-transformers and returns **retrieved excerpts** only (no LLM summary).

---

## API Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check + vector store chunk count |
| POST | `/api/v1/query` | RAG query: `{"question": "...", "top_k": 5}` |
| POST | `/api/v1/ingest` | Upload PDF/TXT/MD (multipart `files`) |
| POST | `/api/v1/ingest/path?directory=...` | Ingest from server path (e.g. `./sample_docs`) |

Full request/response schemas: **http://127.0.0.1:8000/docs**.

---

## MLflow (MLOps)

Query and ingest operations are logged as MLflow runs. To open the MLflow UI:

```bash
mlflow ui --backend-store-uri ./mlruns
```

Then open the URL shown (e.g. http://127.0.0.1:5000) to view runs, parameters, and metrics.

---

## Documentation

- **USER_GUIDE.md** (in `docs/`) — Step-by-step usage and configuration.
- **ARCHITECTURE.md** — Components, data flow, and technology choices.

---

## Ethics and Data Governance

- **Local by default:** Documents and vectors are stored on your machine (ChromaDB).
- **No third-party data sharing** unless you enable OpenAI (embeddings/LLM).
- For production, apply your organization’s policies (data retention, access control, bias monitoring).

---

## Deploy to GitHub & free hosting

- **Push to GitHub:** See **[HOSTING.md](HOSTING.md)** for commands to push this repo to [github.com/sid776/Public_Data_metrics](https://github.com/sid776/Public_Data_metrics).
- **Host the dashboard free:** Use [Streamlit Community Cloud](https://share.streamlit.io/) — connect the GitHub repo, set main file to `dashboard.py`, and deploy. Details in **HOSTING.md**.

---

## License and Disclaimer

This is a **Proof of Concept** for demonstration and evaluation. Not an official World Bank product. Use at your own risk.

---

*Built with Python, FastAPI, ChromaDB, sentence-transformers, and Streamlit.*
