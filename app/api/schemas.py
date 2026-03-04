"""Pydantic schemas for API request/response."""
from typing import List, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request body for /query."""

    question: str = Field(..., min_length=1, description="Natural language question")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of chunks to retrieve")


class SourceChunk(BaseModel):
    """A single retrieved chunk with metadata."""

    text: str
    source: Optional[str] = None
    chunk_index: Optional[int] = None
    distance: Optional[float] = None


class QueryResponse(BaseModel):
    """Response for /query: answer and sources."""

    answer: str
    sources: List[SourceChunk] = Field(default_factory=list)


class IngestResponse(BaseModel):
    """Response after ingesting documents."""

    chunks_ingested: int
    message: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    vector_store_count: int = 0
