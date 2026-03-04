# Document Intelligence — User Guide

## Overview
Document Intelligence is a Proof of Concept (POC) application that lets you upload environmental and social documents (PDF or text), then ask questions in natural language and receive answers backed by the content you uploaded. It uses **RAG** (Retrieval-Augmented Generation), **vector search**, and optional **LLM** integration. A separate **analytics dashboard** shows World Bank data, E&S metrics, and ML/DL analytics (see **Analytics Dashboard** below).

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

---

## Analytics Dashboard

The **Document Intelligence Dashboard** is a separate Streamlit app that combines POC metrics with **real World Bank Open Data**. It uses a **light background** and **muted chart colors**.

### How to run the dashboard
```bash
RUN_DASHBOARD.bat
# or
python -m streamlit run dashboard.py --server.port 8502
```
Open **http://localhost:8502** in your browser.

### Tabs
- **Executive summary** — KPIs and usage by ESF category.
- **World Bank indicators** — Bar charts per indicator (CO₂, Forest, GDP, Life expectancy, Water, Sanitation, etc.) plus stacked bar (GDP, Life exp, Forest).
- **Deep analysis** — Time trends (line/area), rankings, growth rates, GDP vs CO₂ scatter, composite table, heatmap.
- **ML & DL Analytics** — Training curves, Precision/Recall/F1, confusion matrix, feature importance, model comparison.
- **E&S & Safeguards** — Risk coverage and safeguards (sample data).
- **Document intelligence** — Query volume by topic, chunks by source; live chunk count when API is running.
- **Governance & quality** — Data governance and model performance (sample data).

### Sidebar
- **Reporting period** — Last 30 days / 90 days / YTD.
- **Show raw data tables** — Toggles raw tables in some tabs.
- **API status** — Live when `http://127.0.0.1:8000/api/v1/health` is reachable; **Vector store** shows chunk count when Live.
- **Links** — API docs, API root.

### Data
- **World Bank:** API data, cached 1 hour; fallback data used on timeout/failure.
- **Document Intelligence:** Only chunk count is live; other metrics are sample.
- Full details: **docs/DASHBOARD_DETAILS.md**.

---

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
- **README.md** — Setup, run commands, deploy.
- **ARCHITECTURE.md** — System design and data flow.
- **docs/DASHBOARD_DETAILS.md** — Full dashboard documentation (tabs, indicators, charts, data sources, appearance).
- **HOSTING.md** — Push to GitHub and free hosting (e.g. Streamlit Community Cloud).
