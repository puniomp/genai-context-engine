from __future__ import annotations

from context_engine.retrieval.semantic_retriever import SemanticRetriever
from context_engine.orchestration.context_builder import ContextBuilder
from context_engine.serving.llm_client import LLMClient


class AnswerPipeline:
    def __init__(self):
        self.retriever = SemanticRetriever()
        self.context_builder = ContextBuilder()
        self.llm = LLMClient()

    def answer(self, query: str) -> dict:
        chunks = self.retriever.retrieve(query, top_k=5)

        context, metrics = self.context_builder.build_context(chunks)

        prompt = f"""
Answer the question using the provided context.

Context:
{context}

Question:
{query}
"""

        answer = self.llm.generate(prompt)

        return {
            "query": query,
            "answer": answer,
            "retrieved_chunks": len(chunks),
            "context_metrics": metrics,
        }
