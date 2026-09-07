from ai.llm.conversation_service import (
    generate_response,
    close_service,
)


history = [
    {
        "role": "user",
        "content": (
            "I want to improve my English for travelling."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Great. What part of English do you find difficult?"
        ),
    },
    {
        "role": "user",
        "content": (
            "The present perfect tense is confusing."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "I can help you practice it."
        ),
    },
]

try:
    result = generate_response(
        user_message="When should I use it?",
        conversation_history=history,
        update_summary=True,
    )

    print("\n===== FINAL CONVERSATION SERVICE TEST =====")

    print("\nResponse:")
    print(result["response"])

    print("\nNeeds RAG:")
    print(result["needs_rag"])

    print("\nRetrieval Query:")
    print(result["retrieval_query"])

    print("\nSession Summary:")
    print(result["session_summary"])

    print("\nSources:")
    for source in result["sources"]:
        print(source)

    print("\nMetadata:")
    print(result["metadata"])

finally:
    close_service()