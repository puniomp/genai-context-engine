from __future__ import annotations

import uuid

import tiktoken

from context_engine.schemas import Chunk


class TextChunker:
    def __init__(self, chunk_size_tokens: int = 500, overlap_tokens: int = 75):
        if chunk_size_tokens <= 0:
            raise ValueError("chunk_size_tokens must be > 0")
        if overlap_tokens < 0:
            raise ValueError("overlap_tokens must be >= 0")
        if overlap_tokens >= chunk_size_tokens:
            raise ValueError("overlap_tokens must be smaller than chunk_size_tokens")

        self.chunk_size = chunk_size_tokens
        self.overlap = overlap_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def tokenize(self, text: str) -> list[int]:
        return self.tokenizer.encode(text)

    def detokenize(self, tokens: list[int]) -> str:
        return self.tokenizer.decode(tokens)

    def chunk_document(self, doc_id: str, text: str) -> list[Chunk]:
        if not text.strip():
            return []

        tokens = self.tokenize(text)
        chunks: list[Chunk] = []

        start = 0
        chunk_index = 0
        step = self.chunk_size - self.overlap

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            token_slice = tokens[start:end]
            chunk_text = self.detokenize(token_slice).strip()

            if chunk_text:
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        doc_id=doc_id,
                        text=chunk_text,
                        token_count=len(token_slice),
                        chunk_index=chunk_index,
                        metadata={},
                    )
                )
                chunk_index += 1

            if end >= len(tokens):
                break

            start += step

        return chunks
