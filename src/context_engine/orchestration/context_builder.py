from __future__ import annotations

import tiktoken

from context_engine.schemas import RetrievedChunk


class ContextBuilder:
    def __init__(self, max_context_tokens: int = 3000, reserved_response_tokens: int = 800):
        self.max_context_tokens = max_context_tokens
        self.reserved_response_tokens = reserved_response_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def build_context(self, chunks: list[RetrievedChunk]) -> tuple[str, dict]:
        available_tokens = self.max_context_tokens - self.reserved_response_tokens

        included_chunks: list[RetrievedChunk] = []
        total_tokens = 0

        for chunk in chunks:
            chunk_tokens = self.count_tokens(chunk.text)
            if total_tokens + chunk_tokens > available_tokens:
                break

            included_chunks.append(chunk)
            total_tokens += chunk_tokens

        context_parts = []
        for idx, chunk in enumerate(included_chunks, start=1):
            context_parts.append(
                f"[Context {idx} | doc_id={chunk.doc_id} | chunk_id={chunk.chunk_id}]\n{chunk.text}"
            )

        context = "\n\n".join(context_parts)

        metrics = {
            "available_context_tokens": available_tokens,
            "used_context_tokens": total_tokens,
            "included_chunk_count": len(included_chunks),
        }

        return context, metrics
