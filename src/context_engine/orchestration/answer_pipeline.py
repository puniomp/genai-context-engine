from __future__ import annotations

import time

from context_engine.retrieval.semantic_retriever import SemanticRetriever
from context_engine.orchestration.context_builder import ContextBuilder
from context_engine.serving.llm_client import LLMClient


class AnswerPipeline:
    def __init__(self):
        self.retriever = SemanticRetriever()
        self.context_builder = ContextBuilder()
        self.llm = LLMClient()

    def answer(self, query: str, top_k: int = 5) -> dict:
        total_start = time.perf_counter()

        retrieval_start = time.perf_counter()
        chunks = self.retriever.retrieve(query, top_k=top_k)
        retrieval_latency_ms = round((time.perf_counter() - retrieval_start) * 1000, 2)

        context_start = time.perf_counter()
        context, metrics = self.context_builder.build_context(chunks)
        context_build_latency_ms = round((time.perf_counter() - context_start) * 1000, 2)

        prompt = f"""
Answer the question using the provided context.

Context:
{context}

Question:
{query}
"""

        generation_start = time.perf_counter()
        answer = self.llm.generate(prompt)
        generation_latency_ms = round((time.perf_counter() - generation_start) * 1000, 2)

        total_latency_ms = round((time.perf_counter() - total_start) * 1000, 2)

        # Build source previews for debugging retrieval
        sources = []
        for chunk in chunks:
            if isinstance(chunk, dict):
                sources.append({
                    "preview": chunk.get("text", "")[:200],
                    "metadata": chunk.get("metadata", {})
                })
            else:
                sources.append({
                    "preview": str(chunk)[:200]
                })

        return {
            "query": query,
            "answer": answer,
            "retrieved_chunks": len(chunks),
            "context_metrics": metrics,
            "latency_ms": {
                "retrieval": retrieval_latency_ms,
                "context_build": context_build_latency_ms,
                "generation": generation_latency_ms,
                "total": total_latency_ms,
            },
            "top_k": top_k,
            "sources": sources,
        }
