from ai.rag.conditional_retrieval import needs_rag
from ai.rag.query_rewriter import rewrite_query


history = [
    {
        "role": "user",
        "content": "Can you explain the present perfect?"
    },
    {
        "role": "assistant",
        "content": "It is commonly used for experiences and past actions connected to the present."
    }
]


tests = [
    "Hello",
    "How are you?",
    "What is the difference between since and for?",
    "Explain the present perfect tense.",
    "When do I use it?",
]


for message in tests:
    rag_needed = needs_rag(
        message,
        conversation_history=history
    )

    rewritten = rewrite_query(
        message,
        conversation_history=history
    )

    print("\nUser:", message)
    print("Need RAG:", rag_needed)
    print("Query:", rewritten)