"""Vector store using ChromaDB for persistent, in-process storage."""
import uuid
from typing import List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from config.settings import settings
from app.core.embeddings import EmbeddingService


class VectorStore:
    """ChromaDB-backed vector store for document chunks."""

    COLLECTION_NAME = "doc_intelligence"

    def __init__(self, persist_dir: Optional[str] = None):
        self.persist_dir = persist_dir or settings.chroma_persist_dir
        self._client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._embedding_service = EmbeddingService()
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"description": "Document chunks for RAG"},
        )

    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Add document chunks; optionally use precomputed embeddings."""
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        if metadatas is None:
            metadatas = [{}] * len(texts)
        embeddings = self._embedding_service.embed_documents(texts)
        self._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return ids

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[dict] = None,
    ) -> dict:
        """Retrieve closest chunks to query. Returns documents, metadatas, distances."""
        q_embedding = self._embedding_service.embed_query(query_text)
        res = self._collection.query(
            query_embeddings=[q_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        return {
            "documents": res["documents"][0] if res["documents"] else [],
            "metadatas": res["metadatas"][0] if res["metadatas"] else [],
            "distances": res["distances"][0] if res["distances"] else [],
        }

    def count(self) -> int:
        """Approximate number of chunks in the collection."""
        return self._collection.count()

    def clear(self) -> None:
        """Remove all documents (recreate collection)."""
        self._client.delete_collection(self.COLLECTION_NAME)
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"description": "Document chunks for RAG"},
        )
