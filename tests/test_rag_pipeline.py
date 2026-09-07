from ai.rag.rag_pipeline import RAGPipeline


pipeline = RAGPipeline()


# ==========================================================
# TEST 1 — SIMPLE CONVERSATION
# ==========================================================

print("\n")
print("=" * 70)
print("TEST 1 — SIMPLE CONVERSATION")
print("=" * 70)

result = pipeline.process(
    user_message="Hello"
)

print("\nNeeds RAG:")
print(result["needs_rag"])

print("\nRetrieved chunks:")
print(len(result["retrieved_context"]))

print("\nFinal Prompt:")
print(result["final_prompt"])


# ==========================================================
# TEST 2 — ENGLISH LEARNING QUESTION
# ==========================================================

print("\n")
print("=" * 70)
print("TEST 2 — GRAMMAR QUESTION")
print("=" * 70)

result = pipeline.process(
    user_message="When should I use the present perfect tense?"
)

print("\nNeeds RAG:")
print(result["needs_rag"])

print("\nRetrieval Query:")
print(result["retrieval_query"])

print("\nRetrieved chunks:")
print(len(result["retrieved_context"]))


for i, chunk in enumerate(
    result["retrieved_context"],
    start=1,
):
    print(f"\n--- Context {i} ---")

    print(
        "Reranker Score:",
        chunk["reranker_score"],
    )

    print(
        "Category:",
        chunk["metadata"].get("category"),
    )

    print(
        "Source:",
        chunk["metadata"].get("source"),
    )

    print(
        chunk["text"][:300]
    )


# ==========================================================
# TEST 3 — CONVERSATIONAL FOLLOW-UP
# ==========================================================

print("\n")
print("=" * 70)
print("TEST 3 — HISTORY-AWARE FOLLOW-UP")
print("=" * 70)

history = [
    {
        "role": "user",
        "content": "Can you explain the present perfect?"
    },
    {
        "role": "assistant",
        "content": (
            "The present perfect connects past events "
            "with the present."
        )
    },
]

result = pipeline.process(
    user_message="When should I use it?",
    conversation_history=history,
)

print("\nNeeds RAG:")
print(result["needs_rag"])

print("\nCurrent Retrieval Query:")
print(result["retrieval_query"])

print("\nQuery Rewrite Prompt:")
print(result["rewrite_prompt"])

print("\nRetrieved chunks:")
print(len(result["retrieved_context"]))


pipeline.close()