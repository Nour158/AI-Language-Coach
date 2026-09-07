from ai.rag.rag_pipeline import RAGPipeline


pipeline = RAGPipeline()

history = [
    {
        "role": "user",
        "content": "Can you explain the present perfect tense?"
    },
    {
        "role": "assistant",
        "content": (
            "Sure. The present perfect connects a past action "
            "with the present."
        )
    }
]

result = pipeline.process(
    user_message="When should I use it?",
    conversation_history=history,
)

print("\n===== FINAL RESULT =====")
print("Needs RAG:", result["needs_rag"])
print("Retrieval Query:", result["retrieval_query"])
print("Response:", result["response"])
print("Sources:", result["sources"])
print("Metadata:", result["metadata"])

pipeline.close()