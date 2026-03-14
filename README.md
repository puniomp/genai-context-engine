# genai-context-engine

A modular context orchestration engine for large language model applications.

This project implements the core infrastructure required to build scalable retrieval and context construction systems for LLM applications, including document ingestion, semantic indexing, retrieval, and token-aware context construction.

The system demonstrates how modern AI platforms transform unstructured document corpora into structured, semantically searchable context that can be dynamically assembled for LLM inference.

---

# Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt

### 2. Ingest sample documents

python scripts/ingest_corpus.py

Example output:
Document: sample_architecture
chunks: 2

Document: sample_policy
chunks: 2

Total documents: 2
Total chunks: 4

### 3. Start the API server
PYTHONPATH=src uvicorn context_engine.api.main:app --reload

### 4 Query the system
curl -X POST http://127.0.0.1:8000/query \
-H "Content-Type: application/json" \
-d '{"query":"What does this context engine do?","top_k":3}'

Example response:
{
  "query": "What does this context engine do?",
  "answer": "...",
  "retrieved_chunks": 3,
  "context_metrics": {
    "available_context_tokens": 2200,
    "used_context_tokens": 901,
    "included_chunk_count": 3
  },
  "latency_ms": {
    "retrieval": 670,
    "context_build": 28,
    "generation": 4474,
    "total": 5172
  },
  "top_k": 3,
  "sources": [...]
}

# Design Goals

The architecture emphasizes several principles commonly required in production AI systems:

• Modular pipeline components that can be independently replaced or extended  
• Token-aware context construction for efficient LLM utilization  
• Clear separation between ingestion, retrieval, and inference layers  
• Observability hooks for performance and retrieval diagnostics  
• Compatibility with multiple embedding and model providers

# System Architecture

The context engine follows a multi-stage pipeline similar to production AI systems.

          +------------------+
          |  Document Corpus |
          +--------+---------+
                   |
                   v
            +------+------+
            |   Parser    |
            +------+------+
                   |
                   v
            +------+------+
            |  Chunker    |
            +------+------+
                   |
                   v
            +------+------+
            | Embeddings  |
            +------+------+
                   |
                   v
            +------+------+
            | Vector Store|
            +------+------+
                   |
                   v
            +------+------+
            |  Retriever  |
            +------+------+
                   |
                   v
            +------+------+
            | Context     |
            | Builder     |
            +------+------+
                   |
                   v
            +------+------+
            |   LLM       |
            +------+------+
                   |
                   v
             +-----+-----+
             |  FastAPI  |
             |  /query   |
             +-----------+

Each stage is implemented as a modular component to mirror real-world AI infrastructure pipelines.

# Core System Components

The context engine is composed of several modular subsystems:

**Ingestion**
Responsible for parsing raw documents and converting them into structured chunks suitable for semantic indexing.

Files:
src/context_engine/ingestion/parser.py
src/context_engine/ingestion/chunker.py

Capabilities:
document parsing
token-aware chunking
metadata tracking
chunk overlap support

**Embedding Layer**
Transforms chunks into vector embeddings that capture semantic meaning.

File:
src/context_engine/serving/embedding_client.py

Embedding model used: 'text-embedding-3-small'

**Semantic Store**
Maintains a persistent vector index supporting similarity search and metadata storage.

File:
src/context_engine/memory/semantic_store.py

Features:
vector similarity search
metadata storage
persistent local index using Chroma

**Retriever**
Performs semantic search over indexed embeddings to identify relevant knowledge.

File:
src/context_engine/retrieval/semantic_retriever.py

Capabilities:
query embedding generation
vector similarity search
configurable top_k retrieval

**Context Builder**
Constructs token-bounded context windows optimized for LLM inference.

File:
src/context_engine/orchestration/context_builder.py

Responsibilities:
token counting
context packing
prioritizing highest relevance chunks
reserving tokens for model responses

**Answer Pipeline**
Coordinates retrieval and generation.

File:
src/context_engine/orchestration/answer_pipeline.py

Responsibilities:
semantic retrieval
context construction
prompt assembly
LLM inference
latency instrumentation

**Serving Layer**
Provides model interaction interfaces.

Files:
src/context_engine/serving/embedding_client.py
src/context_engine/serving/llm_client.py

**API Layer**
Exposes the system as a service.

File: src/context_engine/api/main.py

Endpoints:
GET  /health
POST /query

**Observability**
Instrumentation for debugging and performance analysis.

Files:
src/context_engine/observability/logging.py
src/context_engine/observability/timing.py

Captured metrics include:
- retrieval latency
- context construction latency
- generation latency
- total request latency

### Evaluation
A lightweight evaluation harness measures answer quality for retrieval queries.

File:
src/context_engine/evaluation/eval_runner.py

Run evaluation:
PYTHONPATH=src python src/context_engine/evaluation/eval_runner.py

Example output:
Query: What does the context engine do?
Score: 0.33

Query: What happens during ingestion?
Score: 1.0

Query: How are documents retrieved?
Score: 1.0

Average score: 0.78

This allows developers to detect regressions when modifying the retrieval or generation pipeline.

---

## Repository Structure

src/context_engine/

    ingestion/        Document parsing and chunking
    memory/           Vector storage layer
    retrieval/        Semantic retrieval logic
    orchestration/    Context construction and prompt assembly
    serving/          Embedding and LLM clients
    observability/    Logging and timing instrumentation
    evaluation/       Evaluation harness
    api/              Service interface

scripts/

    ingest_corpus.py  Document ingestion pipeline

tests/

    Unit and integration tests for core pipeline components

# System Milestones

## Milestone 1 — Document Ingestion & Semantic Retrieval (Complete)

Document ingestion and semantic retrieval pipeline.

Includes:
document parsing
token-aware chunking
embedding generation
vector storage
semantic retrieval

## Milestone 2 — Retrieval-Augmented Generation (Complete)

Integration of retrieval results with LLM inference.
Includes:
context construction
prompt assembly
answer pipeline


## Milestone 3 — API Serving Layer (Complete)

Expose the context engine as a service.

Includes:
FastAPI server
/query endpoint
configurable retrieval parameters
structured response objects

## Milestone 4 — Observability (Complete)

Instrumentation for production diagnostics.

Includes:
latency metrics
retrieval diagnostics
token usage monitoring
query tracing

## Milestone 5 — Evaluation (Complete)

Evaluation harness for measuring retrieval and answer quality.

Includes:
automated evaluation queries
keyword scoring
regression detection

# License
MIT License
Marco Punio — 2026
