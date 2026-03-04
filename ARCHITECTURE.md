# Document Intelligence — Architecture

## Purpose
This document describes the architecture of the Document Intelligence POC: a RAG-based application for querying environmental and social documents via natural language. It is designed to demonstrate AI/ML capabilities relevant to enterprise use cases (e.g. World Bank Group VPU) without requiring Docker or cloud dependencies for local runs.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           User / Client                                   │
│  (Browser – Streamlit UI  or  REST client – e.g. Postman / curl)         │
└────────────────────────────────┬────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FastAPI Application                               │
│  • /api/v1/health   • /api/v1/query   • /api/v1/ingest   • /docs          │
└────────────────────────────────┬────────────────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  RAG Pipeline   │    │ Document        │    │  MLflow          │
│  (retrieve +    │    │ Processor       │    │  (experiment     │
│   generate)     │    │ (chunk PDF/TXT) │    │   tracking)      │
└────────┬────────┘    └────────┬────────┘    └─────────────────┘
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│  Vector Store   │◄───│  Embedding      │
│  (ChromaDB)     │    │  Service        │
│  persistent     │    │  (local / OpenAI)│
└─────────────────┘    └─────────────────┘
```

## Components

### 1. REST API (FastAPI)
- **Technology:** FastAPI, Uvicorn.
- **Endpoints:**
  - `GET /api/v1/health` — Service and vector store status.
  - `POST /api/v1/query` — RAG query (question + optional top_k).
  - `POST /api/v1/ingest` — Upload PDF/TXT/MD; chunk and add to vector store.
  - `POST /api/v1/ingest/path` — Ingest from a server directory (query param).
- **Roles:** API management, integration point for existing systems, OpenAPI documentation.

### 2. RAG Pipeline
- **Retrieve:** Embed the user question, query the vector store for top-k similar chunks.
- **Generate:** Option A — concatenate chunks and (optional) call an LLM for a concise answer. Option B — return retrieved excerpts only (no LLM).
- **Inputs:** User question, config (chunk_size, overlap, top_k).
- **Outputs:** Answer text + list of source chunks with metadata (source file, chunk index, distance).

### 3. Embedding Service
- **Local:** sentence-transformers (e.g. `all-MiniLM-L6-v2`) for embeddings without external API.
- **Optional:** OpenAI text-embedding API when `OPENAI_API_KEY` is set.
- **Interface:** `embed_documents(texts)`, `embed_query(query)`; returns list of vectors.

### 4. Vector Store (ChromaDB)
- **Role:** Persistent vector index of document chunks; in-process, no separate server or Docker.
- **Storage:** Local directory (e.g. `./data/chroma`).
- **Operations:** Add documents (with embeddings and metadata), query by vector (similarity search), count, clear.

### 5. Document Processor
- **Inputs:** PDF, TXT, MD files (path or uploaded bytes).
- **Steps:** Extract text (PyPDF2 for PDF, plain read for TXT/MD), split into overlapping chunks (configurable size/overlap).
- **Outputs:** List of text chunks + list of metadata dicts (source filename, chunk_index).

### 6. MLflow (MLOps)
- **Role:** Experiment tracking and run logging.
- **Logged:** RAG query runs (params: question preview, top_k; metrics: sources_retrieved, answer_length). Ingest runs (params: source_files; metrics: chunks_ingested).
- **Storage:** Local `./mlruns` by default; configurable via `MLFLOW_TRACKING_URI`.

### 7. Streamlit UI
- **Role:** Demo interface for non-technical users.
- **Features:** Ingest (file upload), Ask (question + top_k), About. Calls the FastAPI backend; requires API to be running.

## Data Flow

### Ingest
1. User uploads files (UI or API).
2. Document Processor extracts text and chunks it.
3. Embedding Service produces vectors for each chunk.
4. Vector Store persists chunks + vectors + metadata.
5. (Optional) MLflow logs ingest run.

### Query
1. User sends a question (UI or API).
2. Embedding Service embeds the question.
3. Vector Store returns top-k similar chunks.
4. RAG Pipeline optionally calls LLM with question + context, or returns context only.
5. API returns answer + source chunks.
6. (Optional) MLflow logs query run.

## Technology Choices (No Docker)
- **Python 3.10+** — Single language for API, RAG, and tooling.
- **ChromaDB** — Embedded vector DB; no separate process.
- **sentence-transformers** — Local embeddings; no API key required.
- **FastAPI** — Async-capable, OpenAPI, type hints.
- **MLflow** — File-based tracking by default; no DB or Docker required for POC.

## Security and Ethics (Considerations)
- **Data locality:** Documents and vectors stay on the host unless OpenAI is used (embeddings/LLM).
- **Governance:** Configurable paths and optional logging support audit and data retention policies.
- **Bias and quality:** Model behavior depends on embedding and (if used) LLM; monitoring and evaluation (e.g. via MLflow metrics) support ongoing refinement.

## Scalability and Production
- For production: consider dedicated vector DB (e.g. Pinecone, Weaviate, or managed Chroma), queue-based ingest, auth on API, and cloud deployment (e.g. Azure Container Apps, GCP Run) with Docker if required by the organization.
