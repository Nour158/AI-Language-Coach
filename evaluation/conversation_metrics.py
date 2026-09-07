from __future__ import annotations
import re
from .common_metrics import safe_mean, token_f1

def response_length(text):
    return len(str(text or "").split())

def asks_follow_up_question(text):
    return float("?" in str(text or ""))

def learner_correction_overload(text):
    text = str(text or "").lower()
    correction_markers = (
        "you should say",
        "correct sentence",
        "incorrect",
        "grammar mistake",
        "the correct form",
    )
    return float(any(marker in text for marker in correction_markers))

def reference_similarity(predictions, references):
    return safe_mean(token_f1(p, r) for p, r in zip(predictions, references))

def aggregate_conversation_quality(responses):
    responses = list(responses)
    return {
        "count": len(responses),
        "avg_response_words": round(safe_mean(response_length(x) for x in responses), 2),
        "follow_up_question_rate": round(safe_mean(asks_follow_up_question(x) for x in responses), 4),
        "correction_overload_rate": round(safe_mean(learner_correction_overload(x) for x in responses), 4),
    }
