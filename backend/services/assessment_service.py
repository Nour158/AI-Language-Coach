from typing import List

from backend.schemas.chat import Message


def evaluate_session(history: List[Message]) -> dict:
    """
    Temporary Role 2 integration point.

    Replace this mock implementation later with:
        evaluate_session(conversation_history)

    Keep the returned keys stable so React does not need to change.
    """
    learner_messages = [m.content for m in history if m.role == "user"]

    if not learner_messages:
        return {
            "overall_score": 0,
            "cefr_level": None,
            "scores": {
                "grammar": 0,
                "vocabulary": 0,
                "fluency": 0,
                "coherence": 0,
                "sentence_structure": 0,
            },
            "strengths": [],
            "weaknesses": ["No learner messages were available to assess."],
            "mistakes": [],
            "repeated_patterns": [],
            "exercises": [],
            "source": "mock",
        }

    return {
        "overall_score": 78,
        "cefr_level": None,
        "scores": {
            "grammar": 75,
            "vocabulary": 82,
            "fluency": 78,
            "coherence": 80,
            "sentence_structure": 76,
        },
        "strengths": [
            "Good participation in the conversation.",
            "Ideas are generally easy to understand."
        ],
        "weaknesses": [
            "Past-tense consistency may need more practice."
        ],
        "mistakes": [
            {
                "original": "Yesterday I go to university.",
                "corrected": "Yesterday I went to university.",
                "natural_alternative": "I went to university yesterday.",
                "category": "Grammar",
                "explanation": "Use the past tense for a completed action in the past."
            }
        ],
        "repeated_patterns": [
            "Possible tense inconsistency"
        ],
        "exercises": [
            "Write 5 sentences about what you did yesterday using past-tense verbs."
        ],
        "source": "mock",
    }
