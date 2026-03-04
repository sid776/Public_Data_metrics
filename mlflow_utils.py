"""MLflow integration for experiment tracking and model logging (MLOps)."""
import os
from pathlib import Path

import mlflow
from config.settings import settings


def get_mlflow_client():
    """Return MLflow client with project tracking URI."""
    uri = settings.mlflow_tracking_uri
    Path(uri).mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"file:///{uri.replace(os.sep, '/')}")
    return mlflow


def log_rag_run(question: str, top_k: int, num_sources: int, answer_len: int):
    """Log a RAG query as an MLflow run (metrics + params)."""
    client = get_mlflow_client()
    with mlflow.start_run(run_name="rag_query"):
        mlflow.log_param("question_preview", question[:100] if question else "")
        mlflow.log_param("top_k", top_k)
        mlflow.log_metric("sources_retrieved", num_sources)
        mlflow.log_metric("answer_length", answer_len)


def log_ingest_run(num_chunks: int, source_files: int):
    """Log a document ingestion run."""
    client = get_mlflow_client()
    with mlflow.start_run(run_name="ingest"):
        mlflow.log_param("source_files", source_files)
        mlflow.log_metric("chunks_ingested", num_chunks)
