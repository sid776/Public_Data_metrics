"""
Document Intelligence — Streamlit UI
RAG-powered Q&A for environmental and social documents. POC for World Bank AI use cases.
"""
import requests
import streamlit as st

st.set_page_config(
    page_title="Document Intelligence | RAG POC",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://127.0.0.1:8000"

# Custom CSS for a polished, professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #0d47a1 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(13, 71, 161, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-weight: 700;
        font-size: 1.8rem;
    }
    .main-header p {
        margin: 0.4rem 0 0 0;
        opacity: 0.95;
        font-size: 0.95rem;
    }
    .source-card {
        background: #f8fafc;
        border-left: 4px solid #1565c0;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
    }
    .answer-box {
        background: linear-gradient(180deg, #e3f2fd 0%, #f5f9ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #bbdefb;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        box-shadow: 0 4px 12px rgba(21, 101, 192, 0.4);
    }
</style>
""", unsafe_allow_html=True)


def api_health():
    try:
        r = requests.get(f"{API_BASE}/api/v1/health", timeout=3)
        return r.status_code == 200, r.json() if r.ok else {}
    except Exception:
        return False, {}


def api_query(question: str, top_k: int = 5):
    try:
        r = requests.post(
            f"{API_BASE}/api/v1/query",
            json={"question": question, "top_k": top_k},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"answer": f"Error: {e}", "sources": []}


def api_ingest(file_list):
    """Upload files to API; FastAPI expects multiple 'files' form keys."""
    try:
        multipart = [("files", (f.name, f.getvalue())) for f in file_list]
        r = requests.post(f"{API_BASE}/api/v1/ingest", files=multipart, timeout=120)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"chunks_ingested": 0, "message": str(e)}


st.markdown(
    '<div class="main-header">'
    '<h1>📄 Document Intelligence</h1>'
    '<p>RAG-powered Q&A for environmental and social documents — Proof of Concept for AI/ML workflows</p>'
    '</div>',
    unsafe_allow_html=True,
)

ok, health = api_health()
if not ok:
    st.warning("⚠️ API is not running. Start it with: `python run_api.py` then refresh this page.")
    st.stop()

sidebar = st.sidebar
sidebar.metric("Vector store chunks", health.get("vector_store_count", 0))

tab_query, tab_ingest, tab_about = st.tabs(["Ask a question", "Ingest documents", "About"])

with tab_query:
    question = st.text_area(
        "Ask a question about your ingested documents",
        placeholder="e.g. What are the main environmental risks mentioned? What social safeguards are recommended?",
        height=100,
    )
    top_k = st.slider("Number of source chunks to retrieve", 1, 15, 5)
    if st.button("Get answer"):
        if not question.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Retrieving and generating answer..."):
                result = api_query(question.strip(), top_k=top_k)
            st.markdown("### Answer")
            st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
            if result.get("sources"):
                st.markdown("### Source excerpts")
                for i, src in enumerate(result["sources"], 1):
                    label = f"**{i}.**"
                    if isinstance(src, dict):
                        text = src.get("text", str(src))
                        source = src.get("source", "")
                    else:
                        text = getattr(src, "text", str(src))
                        source = getattr(src, "source", "") or ""
                    if source:
                        label += f" *{source}*"
                    st.markdown(label)
                    st.markdown(f'<div class="source-card">{text[:500]}{"..." if len(str(text)) > 500 else ""}</div>', unsafe_allow_html=True)

with tab_ingest:
    st.markdown("Upload PDF or TXT files to add them to the vector store. Then use the **Ask a question** tab.")
    uploaded = st.file_uploader("Choose files", type=["pdf", "txt", "md"], accept_multiple_files=True)
    if st.button("Ingest uploaded files") and uploaded:
        with st.spinner("Chunking and embedding..."):
            out = api_ingest(uploaded)
        st.success(out.get("message", f"Ingested {out.get('chunks_ingested', 0)} chunks."))
    elif uploaded and st.button("Ingest uploaded files"):
        st.info("Select at least one file.")

with tab_about:
    st.markdown("""
    ### About this POC
    This **Document Intelligence** app demonstrates:
    - **RAG (Retrieval-Augmented Generation)** over your documents
    - **Vector search** (ChromaDB) and semantic embeddings (sentence-transformers or OpenAI)
    - **REST API** (FastAPI) for integration into existing systems
    - **MLflow** for experiment and run tracking (MLOps)
    - **Ethics & governance**: local-first option, configurable data retention, no training on your data

    *Built as a Proof of Concept for AI use cases in environmental and social applications.*
    """)
