from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI


class EmbeddingClient:
    def __init__(self, model: str = "text-embedding-3-small"):
        load_dotenv(dotenv_path=".env")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=[query],
        )
        return response.data[0].embedding
