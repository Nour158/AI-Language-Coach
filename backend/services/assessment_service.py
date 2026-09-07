from ai.assessment.session_evaluator import evaluate_session

class AssessmentService:
    def evaluate(self, conversation_history):
        return evaluate_session(conversation_history)

assessment_service = AssessmentService()
