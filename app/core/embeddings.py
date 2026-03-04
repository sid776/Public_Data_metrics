"""Embedding service: local (sentence-transformers) and optional OpenAI."""
from typing import List

from config.settings import settings


class EmbeddingService:
    """Generate text embeddings via local model or OpenAI."""

    def __init__(self):
        self._model = None
        self._use_openai = getattr(settings, "use_openai_embeddings", False) and bool(
            getattr(settings, "openai_api_key", "")
        )

    def _get_local_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(settings.embedding_model)
        return self._model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts; returns list of vectors."""
        if self._use_openai:
            return self._embed_openai(texts)
        model = self._get_local_model()
        vectors = model.encode(texts, convert_to_numpy=True)
        return vectors.tolist()

    def embed_query(self, query: str) -> List[float]:
        """Embed a single query string."""
        return self.embed_documents([query])[0]

    def _embed_openai(self, texts: List[str]) -> List[List[float]]:
        import openai
        client = openai.OpenAI(api_key=settings.openai_api_key)
        model = getattr(settings, "embedding_model", "text-embedding-3-small")
        if "sentence-transformers" in model:
            model = "text-embedding-3-small"
        out = client.embeddings.create(input=texts, model=model)
        return [e.embedding for e in out.data]

    @property
    def dimension(self) -> int:
        """Embedding dimension for the current backend."""
        if self._use_openai:
            return len(self.embed_query("dummy"))
        return self._get_local_model().get_sentence_embedding_dimension()
