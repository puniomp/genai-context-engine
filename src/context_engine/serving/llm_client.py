from __future__ import annotations

import os
from dotenv import load_dotenv
from openai import OpenAI


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        load_dotenv(".env")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        return response.choices[0].message.content
