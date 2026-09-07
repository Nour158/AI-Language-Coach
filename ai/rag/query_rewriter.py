class QueryRewriter:
    """
    Creates a standalone retrieval query using conversation history.
    """

    def build_rewrite_prompt(
        self,
        user_message,
        conversation_history,
    ):
        if not conversation_history:
            return user_message

        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in conversation_history
        )

        return f"""
Rewrite the user's latest message as a standalone search query.

Use the conversation history only to resolve missing context,
pronouns, or references.

Do not answer the question.
Do not add information that the user did not provide.

Conversation history:
{history_text}

Latest user message:
{user_message}

Standalone search query:
""".strip()