from typing import List, Any

from ai.assessment.session_evaluator import evaluate_session


class AssessmentService:
    """
    Backend service wrapper around the real Role 2 assessment pipeline.
    """

    def evaluate(self, conversation_history: List[Any]) -> dict:
        """
        Evaluate a completed learner conversation.

        Parameters
        ----------
        conversation_history:
            Conversation messages passed from the backend/session layer.

        Returns
        -------
        dict
            Structured learner assessment report.
        """
        return evaluate_session(conversation_history)


assessment_service = AssessmentService()
