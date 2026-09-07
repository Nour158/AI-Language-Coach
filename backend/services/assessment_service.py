from typing import List, Any

from ai.assessment.session_evaluator import evaluate_session


class AssessmentService:
    """
    Backend service wrapper around the real Role 2 assessment pipeline.
    """

    def evaluate(self, conversation_history: List[Any]) -> dict:
        return evaluate_session(conversation_history)


assessment_service = AssessmentService()
