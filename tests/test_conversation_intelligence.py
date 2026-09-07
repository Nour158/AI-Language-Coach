from ai.llm.memory import ConversationMemory
from ai.llm.session_summary import SessionSummarizer
from ai.rag.query_rewriter import QueryRewriter
from ai.rag.conditional_retrieval import ConditionalRetrieval


print("\n===== MEMORY TEST =====")

memory = ConversationMemory(max_messages=10)

memory.add_message(
    "user",
    "Can you explain the present perfect?"
)

memory.add_message(
    "assistant",
    "Sure! The present perfect connects the past with the present."
)

memory.add_message(
    "user",
    "When should I use it?"
)

for message in memory.get_recent_history():
    print(message)


print("\n===== CONDITIONAL RAG TEST =====")

conditional = ConditionalRetrieval()

test_messages = [
    "Hello",
    "Thanks",
    "When should I use the present perfect?",
    "Explain the difference between since and for",
]

for message in test_messages:
    print(
        message,
        "-> RAG:",
        conditional.should_retrieve(message)
    )


print("\n===== QUERY REWRITER PROMPT TEST =====")

rewriter = QueryRewriter()

history = memory.get_recent_history()[:-1]

rewrite_prompt = rewriter.build_rewrite_prompt(
    user_message="When should I use it?",
    conversation_history=history,
)

print(rewrite_prompt)


print("\n===== SESSION SUMMARY PROMPT TEST =====")

summarizer = SessionSummarizer()

summary_prompt = summarizer.build_summary_prompt(
    memory.get_recent_history()
)

print(summary_prompt)