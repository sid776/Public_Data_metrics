"""API route handlers."""
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.schemas import (
    QueryRequest,
    QueryResponse,
    SourceChunk,
    IngestResponse,
    HealthResponse,
)
from app.core.rag import RAGPipeline
from app.core.vector_store import VectorStore
from app.services.document_processor import DocumentProcessor

router = APIRouter(prefix="/api/v1", tags=["document-intelligence"])


def _log_rag_mlflow(question: str, top_k: int, num_sources: int, answer_len: int):
    try:
        from mlflow_utils import log_rag_run
        log_rag_run(question, top_k, num_sources, answer_len)
    except Exception:
        pass


def _log_ingest_mlflow(chunks: int, files: int):
    try:
        from mlflow_utils import log_ingest_run
        log_ingest_run(chunks, files)
    except Exception:
        pass


def _get_rag() -> RAGPipeline:
    return RAGPipeline()


def _get_store() -> VectorStore:
    return VectorStore()


@router.get("/health", response_model=HealthResponse)
def health():
    """Health check and vector store status."""
    store = _get_store()
    return HealthResponse(
        status="ok",
        vector_store_count=store.count(),
    )


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    """RAG query: natural language question -> answer with sources."""
    rag = _get_rag()
    result = rag.query(question=req.question, top_k=req.top_k)
    metas = result.get("metadatas") or []
    dists = result.get("distances") or []
    sources = [
        SourceChunk(
            text=text,
            source=metas[i].get("source") if i < len(metas) else None,
            chunk_index=metas[i].get("chunk_index") if i < len(metas) else None,
            distance=dists[i] if i < len(dists) else None,
        )
        for i, text in enumerate(result.get("sources") or [])
    ]
    _log_rag_mlflow(req.question, req.top_k or 5, len(sources), len(result["answer"]))
    return QueryResponse(answer=result["answer"], sources=sources)


@router.post("/ingest", response_model=IngestResponse)
async def ingest(files: List[UploadFile] = File(...)):
    """Upload PDF/TXT files; chunk and add to vector store."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    store = _get_store()
    total = 0
    for uf in files:
        suffix = Path(uf.filename or "").suffix.lower()
        if suffix not in (".pdf", ".txt", ".md"):
            continue
        content = await uf.read()
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)
        try:
            chunks, metadatas = DocumentProcessor.process_file(tmp_path)
            if chunks:
                store.add_documents(chunks, metadatas=metadatas)
                total += len(chunks)
        finally:
            tmp_path.unlink(missing_ok=True)
    _log_ingest_mlflow(total, len(files))
    return IngestResponse(
        chunks_ingested=total,
        message=f"Ingested {total} chunks from {len(files)} file(s).",
    )


@router.post("/ingest/path", response_model=IngestResponse)
def ingest_path(directory: str = ""):
    """Ingest all PDF/TXT/MD files from a directory (query: ?directory=./docs). For demo/dev."""
    if not directory:
        raise HTTPException(status_code=400, detail="Query parameter 'directory' required")
    path = Path(directory)
    if not path.is_dir():
        raise HTTPException(status_code=400, detail="Not a directory")
    chunks, metadatas = DocumentProcessor.process_directory(path)
    if not chunks:
        return IngestResponse(chunks_ingested=0, message="No supported files found.")
    store = _get_store()
    store.add_documents(chunks, metadatas=metadatas)
    _log_ingest_mlflow(len(chunks), 1)
    return IngestResponse(
        chunks_ingested=len(chunks),
        message=f"Ingested {len(chunks)} chunks from {directory}.",
    )
