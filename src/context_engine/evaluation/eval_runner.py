from context_engine.orchestration.answer_pipeline import AnswerPipeline


tests = [
    {
        "query": "What does the context engine do?",
        "expected_keywords": ["retrieval", "context", "embeddings"]
    },
    {
        "query": "What happens during ingestion?",
        "expected_keywords": ["documents", "chunk", "embedding"]
    },
    {
        "query": "How are documents retrieved?",
        "expected_keywords": ["similarity", "vector", "chunks"]
    }
]


def run_eval():
    pipeline = AnswerPipeline()

    results = []

    for test in tests:
        result = pipeline.answer(test["query"])
        answer = result["answer"].lower()

        score = sum(
            keyword in answer
            for keyword in test["expected_keywords"]
        ) / len(test["expected_keywords"])

        results.append(score)

        print("Query:", test["query"])
        print("Score:", score)
        print("Answer preview:", answer[:200])
        print("-" * 50)

    avg_score = sum(results) / len(results)
    print("Average score:", round(avg_score, 2))


if __name__ == "__main__":
    run_eval()
