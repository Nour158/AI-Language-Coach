class ConversationPromptBuilder:
    """
    Builds the final prompt that will be sent to the LLM.
    """

    def __init__(self):
        self.system_prompt = """
You are an AI English Language Coach.

Your job is to help the learner practice English naturally and confidently.

Rules:
- Keep the conversation natural and engaging.
- Encourage the learner to continue speaking.
- Do not correct every mistake automatically.
- Correct mistakes only when useful, important, or requested.
- Give clear explanations appropriate to the learner's level.
- Use retrieved educational context when relevant.
- Do not invent information that is not supported by the context.
- If retrieved context is not useful, rely on general conversational ability.
- Keep responses concise unless the learner asks for more detail.
""".strip()

    def build_prompt(
        self,
        user_message,
        conversation_history=None,
        session_summary="",
        retrieved_context=None,
    ):
        conversation_history = conversation_history or []
        retrieved_context = retrieved_context or []

        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in conversation_history
        )

        rag_text = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_context
            if chunk.get("text")
        )

        prompt_parts = [
            f"SYSTEM:\n{self.system_prompt}"
        ]

        if session_summary:
            prompt_parts.append(
                f"SESSION SUMMARY:\n{session_summary}"
            )

        if rag_text:
            prompt_parts.append(
                f"RETRIEVED KNOWLEDGE:\n{rag_text}"
            )

        if history_text:
            prompt_parts.append(
                f"RECENT CONVERSATION:\n{history_text}"
            )

        prompt_parts.append(
            f"USER MESSAGE:\n{user_message}"
        )

        prompt_parts.append(
            """
INSTRUCTION:
Respond naturally as an English language coach.
Use the retrieved knowledge only if it helps answer the learner.
""".strip()
        )

        return "\n\n".join(prompt_parts)