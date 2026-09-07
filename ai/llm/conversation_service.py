from ai.rag.rag_pipeline import RAGPipeline
from ai.llm.session_summary import SessionSummaryGenerator


class ConversationService:
    """
    High-level conversation service for the AI Language Coach.

    This is the main interface used by the backend.

    Responsibilities:
    - receive the user message
    - receive conversation history
    - optionally update the session summary
    - run the complete conversational RAG pipeline
    - return JSON-friendly structured output
    """

    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        self.summary_generator = SessionSummaryGenerator()

    def generate_response(
        self,
        user_message,
        conversation_history=None,
        session_summary="",
        update_summary=False,
    ):
        conversation_history = conversation_history or []

        updated_summary = session_summary

        # ---------------------------------------------
        # 1. Optionally update session summary
        # ---------------------------------------------

        if update_summary and conversation_history:
            try:
                updated_summary = (
                    self.summary_generator.generate_summary(
                        conversation_history=conversation_history,
                        previous_summary=session_summary,
                    )
                )
            except Exception as exc:
                print(
                    "Warning: session summary generation failed."
                )
                print(exc)

        # ---------------------------------------------
        # 2. Run complete RAG + Qwen pipeline
        # ---------------------------------------------

        result = self.rag_pipeline.process(
            user_message=user_message,
            conversation_history=conversation_history,
            session_summary=updated_summary,
        )

        # ---------------------------------------------
        # 3. Add summary to structured response
        # ---------------------------------------------

        result["session_summary"] = updated_summary

        return result

    def close(self):
        self.rag_pipeline.close()


# -----------------------------------------------------
# Stable project-level function
# -----------------------------------------------------

_service = None


def generate_response(
    user_message,
    conversation_history=None,
    session_summary="",
    update_summary=False,
):
    """
    Stable interface required by the project.

    Example:

        result = generate_response(
            user_message="When should I use it?",
            conversation_history=[...]
        )

    Returns a JSON-friendly dictionary.
    """

    global _service

    if _service is None:
        _service = ConversationService()

    return _service.generate_response(
        user_message=user_message,
        conversation_history=conversation_history,
        session_summary=session_summary,
        update_summary=update_summary,
    )
def close_service():
    """
    Close resources used by the shared ConversationService.
    """

    global _service

    if _service is not None:
        _service.close()
        _service = None