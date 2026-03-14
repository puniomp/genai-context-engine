from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    doc_id: str
    title: str
    source_path: str
    content_type: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)


class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    token_count: int
    chunk_index: int
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    retrieved_chunks: list[RetrievedChunk]
    metrics: dict[str, Any] = Field(default_factory=dict)

