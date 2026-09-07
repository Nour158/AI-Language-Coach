from ai.prompts.conversation_prompts import ConversationPromptBuilder


builder = ConversationPromptBuilder()

history = [
    {
        "role": "user",
        "content": "Can you explain the present perfect?"
    },
    {
        "role": "assistant",
        "content": "Sure. It connects past actions with the present."
    },
]

retrieved_context = [
    {
        "text": (
            "Present Perfect: I have eaten sushi. "
            "This tense can connect past events with the present."
        )
    },
    {
        "text": (
            "Signal words for the present perfect may include "
            "since, for, already, yet, and ever."
        )
    },
]

prompt = builder.build_prompt(
    user_message="When should I use it?",
    conversation_history=history,
    session_summary=(
        "The learner is practicing English grammar "
        "and is currently discussing the present perfect."
    ),
    retrieved_context=retrieved_context,
)

print("\n===== FINAL CONVERSATION PROMPT =====\n")
print(prompt)