# Document Intelligence — User Guide

## Overview
Document Intelligence is a Proof of Concept (POC) application that lets you upload environmental and social documents (PDF or text), then ask questions in natural language and receive answers backed by the content you uploaded. It uses **RAG** (Retrieval-Augmented Generation), **vector search**, and optional **LLM** integration.

## Quick Start

### 1. Install dependencies
```bash
cd WB_POC
pip install -r requirements.txt
```

### 2. Start the API
```bash
python run_api.py
```
The API will be available at **http://127.0.0.1:8000**. Open **http://127.0.0.1:8000/docs** for interactive API documentation.

### 3. Start the web UI (optional)
In a second terminal:
```bash
python run_ui.py
```
Then open **http://localhost:8501** in your browser.

### 4. Ingest sample documents
- **Via UI:** Go to the "Ingest documents" tab, upload the files in `sample_docs/`, and click "Ingest uploaded files."
- **Via API:** Use the `/api/v1/ingest` endpoint with multipart form data (see `/docs`).

### 5. Ask questions
- **Via UI:** Use the "Ask a question" tab (e.g. "What are the main environmental risks?" or "What is required for involuntary resettlement?").
- **Via API:** `POST /api/v1/query` with JSON body `{"question": "...", "top_k": 5}`.

## Configuration
- Copy `.env.example` to `.env` and optionally set:
  - **OPENAI_API_KEY** — Enables OpenAI embeddings and/or LLM for higher-quality answers.
  - **CHROMA_PERSIST_DIR** — Where vector data is stored (default: `./data/chroma`).
  - **MLFLOW_TRACKING_URI** — Where MLflow logs runs (default: `./mlruns`).

Without an OpenAI key, the app uses local sentence-transformers for embeddings and returns retrieved excerpts without an LLM-generated summary.

## MLflow (MLOps)
RAG queries and ingest runs are logged as MLflow runs (when the tracking URI is set). To view:
```bash
mlflow ui --backend-store-uri ./mlruns
```
Then open the URL shown (e.g. http://127.0.0.1:5000).

## Ethics and data
- Data is stored locally by default (ChromaDB on disk).
- No document content is sent to third parties unless you enable OpenAI (embeddings/LLM).
- For production, consider data retention policies and access controls as per your organization’s AI governance.

## Support
See **README.md** and **ARCHITECTURE.md** for setup details, architecture, and technical specifications.
