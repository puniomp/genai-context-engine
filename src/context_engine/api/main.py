from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from context_engine.orchestration.answer_pipeline import AnswerPipeline


pipeline: Optional[AnswerPipeline] = None


class QueryRequest(BaseModel):
    query: str = Field(..., description="User query to answer")
    top_k: int = Field(default=5, ge=1, le=25, description="Number of chunks to retrieve")
    max_context_tokens: Optional[int] = Field(
        default=None,
        ge=1,
        description="Optional context token budget override",
    )


class QueryResponse(BaseModel):
    query: str
    answer: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


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
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline is not initialized.")

    try:
        result = pipeline.answer(request.query)

        if isinstance(result, str):
            return QueryResponse(
                query=request.query,
                answer=result,
                metadata={},
            )

        if isinstance(result, dict):
            return QueryResponse(
                query=request.query,
                answer=result.get("answer", ""),
                metadata={k: v for k, v in result.items() if k != "answer"},
            )

        raise HTTPException(
            status_code=500,
            detail="Unexpected pipeline response format.",
        )

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Query execution failed: {str(exc)}",
        ) from exc
