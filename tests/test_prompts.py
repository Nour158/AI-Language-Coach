from ai.prompts.conversation_prompts import build_messages


history = [
    {
        "role": "user",
        "content": "Can you explain the present perfect?"
    },
    {
        "role": "assistant",
        "content": "Sure. We often use it for past events connected to the present."
    }
]


messages = build_messages(
    user_message="When do I use it?",
    conversation_history=history,
    session_summary="The learner is practicing English grammar.",
    rag_context=(
        "Present perfect is commonly used for experiences, "
        "unfinished time periods, and past actions connected "
        "to the present."
    ),
)


for message in messages:
    print("\nROLE:", message["role"])
    print(message["content"])