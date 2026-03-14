from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from context_engine.orchestration.answer_pipeline import AnswerPipeline


pipeline: Optional[AnswerPipeline] = None


class QueryRequest(BaseModel):
    query: str = Field(..., description="User query to answer")
    top_k: int = Field(default=5, ge=1, le=25, description="Number of chunks to retrieve")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline
    pipeline = AnswerPipeline()
    yield
    pipeline = None


app = FastAPI(
    title="genai-context-engine",
    version="0.1.0",
    description="Context orchestration API for retrieval-augmented query answering.",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query")
def query(request: QueryRequest):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline is not initialized.")

    try:
        return pipeline.answer(request.query, top_k=request.top_k)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Query execution failed: {str(exc)}",
        ) from exc