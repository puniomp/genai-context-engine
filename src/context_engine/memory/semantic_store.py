from __future__ import annotations

from typing import Iterable

import chromadb
from chromadb.api.models.Collection import Collection

from context_engine.schemas import Chunk, RetrievedChunk
from context_engine.serving.embedding_client import EmbeddingClient


class SemanticStore:
    def __init__(
        self,
        persist_directory: str = "data/processed/chroma",
        collection_name: str = "document_chunks",
        embedding_client: EmbeddingClient | None = None,
    ):
        self.client = chromadb.PersistentClient(path=persist_directory)

        self.collection: Collection = self.client.get_or_create_collection(
            name=collection_name
        )

        self.embedding_client = embedding_client or EmbeddingClient()

    def add_chunks(self, chunks: Iterable[Chunk]) -> int:
        chunk_list = list(chunks)
        if not chunk_list:
            return 0

        ids = [chunk.chunk_id for chunk in chunk_list]
        documents = [chunk.text for chunk in chunk_list]

        metadatas = [
            {
                "doc_id": chunk.doc_id,
                "chunk_index": chunk.chunk_index,
                "token_count": chunk.token_count,
            }
            for chunk in chunk_list
        ]

        embeddings = self.embedding_client.embed_texts(documents)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        return len(chunk_list)

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        query_embedding = self.embedding_client.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        retrieved_chunks = []

        for chunk_id, text, meta, dist in zip(ids, docs, metas, distances):
            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    doc_id=meta["doc_id"],
                    text=text,
                    score=float(dist),
                    metadata=meta,
                )
            )

        return retrieved_chunks

