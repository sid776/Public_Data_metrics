"""Application configuration with environment variable support."""
import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Centralized settings for the Document Intelligence POC."""

    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = Path(__file__).resolve().parent.parent / "data"
    chroma_persist_dir: str = ""
    mlflow_tracking_uri: str = ""

    # Embeddings & LLM
    openai_api_key: str = ""
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    use_openai_embeddings: bool = False
    use_openai_llm: bool = False

    # RAG
    chunk_size: int = 800
    chunk_overlap: int = 100
    top_k_retrieve: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.chroma_persist_dir:
            self.chroma_persist_dir = str(self.data_dir / "chroma")
        if not self.mlflow_tracking_uri:
            self.mlflow_tracking_uri = str(self.base_dir / "mlruns")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        Path(self.chroma_persist_dir).mkdir(parents=True, exist_ok=True)


settings = Settings()
