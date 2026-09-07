from ai.llm.qwen_client import QwenClient


class SessionSummaryGenerator:
    """
    Creates a compact summary of the learner's conversation session.

    The summary keeps useful long-term context such as:
    - learner goals
    - English level
    - topics discussed
    - recurring language difficulties
    - preferences
    - useful conversation context
    """

    def __init__(self):
        self.qwen = QwenClient()

    def build_summary_prompt(
        self,
        conversation_history,
        previous_summary="",
    ):
        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in conversation_history
        )

        return f"""
You are summarizing an English learner's conversation session.

Keep only information that may help the AI coach in future conversation.

Include, when available:
- learner goals
- estimated English level
- topics discussed
- preferences
- recurring grammar or vocabulary difficulties
- important personal conversation context

Do not include unnecessary details.
Do not invent information.
Keep the summary concise.

PREVIOUS SESSION SUMMARY:
{previous_summary if previous_summary else "None"}

RECENT CONVERSATION:
{history_text}

Return only the updated summary.
""".strip()

    def generate_summary(
        self,
        conversation_history,
        previous_summary="",
    ):
        if not conversation_history:
            return previous_summary

        prompt = self.build_summary_prompt(
            conversation_history=conversation_history,
            previous_summary=previous_summary,
        )

        summary = self.qwen.generate(
            prompt,
            max_new_tokens=180,
        )

        return summary.strip()

# Backward-compatible name used by existing tests/integration
SessionSummarizer = SessionSummaryGenerator
