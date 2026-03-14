from __future__ import annotations

from context_engine.memory.semantic_store import SemanticStore
from context_engine.schemas import RetrievedChunk


class SemanticRetriever:
    def __init__(self, store: SemanticStore | None = None):
        self.store = store or SemanticStore()

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        return self.store.search(query=query, top_k=top_k)
