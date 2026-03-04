"""RAG pipeline: retrieve relevant chunks and generate answers (optional LLM)."""
from typing import List, Optional

from config.settings import settings
from app.core.vector_store import VectorStore
from app.core.embeddings import EmbeddingService


class RAGPipeline:
    """Retrieval-Augmented Generation: retrieve context and optionally use LLM for answer."""

    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding_service = EmbeddingService()
        self._use_llm = getattr(settings, "use_openai_llm", False) and bool(
            getattr(settings, "openai_api_key", "")
        )

    def retrieve(self, query: str, top_k: Optional[int] = None) -> dict:
        """Retrieve top-k relevant chunks for a query."""
        k = top_k or settings.top_k_retrieve
        return self.vector_store.query(query_text=query, n_results=k)

    def generate_answer(
        self,
        query: str,
        context_chunks: List[str],
        use_llm: Optional[bool] = None,
    ) -> str:
        """Generate answer from query and context. If no LLM, return summarized context."""
        use_llm = use_llm if use_llm is not None else self._use_llm
        context = "\n\n---\n\n".join(context_chunks)
        if use_llm:
            return self._call_llm(query, context)
        return self._format_context_only(query, context)

    def _call_llm(self, query: str, context: str) -> str:
        import openai
        client = openai.OpenAI(api_key=settings.openai_api_key)
        prompt = f"""You are an assistant for environmental and social specialists. Use only the following context to answer the question. If the context does not contain enough information, say so.

Context:
{context}

Question: {query}

Answer (concise, cite the context where relevant):"""
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        return resp.choices[0].message.content or "No response."

    def _format_context_only(self, query: str, context: str) -> str:
        if not context.strip():
            return "No relevant documents found. Try adding more documents or rephrasing your question."
        return (
            "Relevant excerpts from the documents (no LLM configured; add OPENAI_API_KEY for full RAG):\n\n"
            + context
        )

    def query(self, question: str, top_k: Optional[int] = None) -> dict:
        """Full RAG: retrieve + generate answer. Returns answer and sources."""
        retrieved = self.retrieve(question, top_k=top_k)
        chunks = retrieved.get("documents") or []
        answer = self.generate_answer(question, chunks)
        return {
            "answer": answer,
            "sources": chunks,
            "metadatas": retrieved.get("metadatas") or [],
            "distances": retrieved.get("distances") or [],
        }
