from .config import (
    DIMENSION_WEIGHTS, NLP_WEIGHT, LLM_WEIGHT,
    MIN_EVIDENCE_WORDS_FOR_LEVEL_HINT, MIN_EVIDENCE_TURNS_FOR_LEVEL_HINT,
)
from .schemas import clamp_score

class ProficiencyScorer:
    def blend_dimension(self, heuristic_score, llm_score):
        if llm_score is None:
            return clamp_score(heuristic_score)
        return clamp_score(
            (heuristic_score * NLP_WEIGHT + llm_score * LLM_WEIGHT)
            / (NLP_WEIGHT + LLM_WEIGHT)
        )

    def overall(self, scores):
        total = 0.0
        used = 0.0
        for dimension, weight in DIMENSION_WEIGHTS.items():
            if dimension in scores:
                total += clamp_score(scores[dimension]) * weight
                used += weight
        return clamp_score(total / used if used else 0)

    def cefr_result(self, learner_words, learner_turns, llm_hint=None):
        if (learner_words < MIN_EVIDENCE_WORDS_FOR_LEVEL_HINT or
                learner_turns < MIN_EVIDENCE_TURNS_FOR_LEVEL_HINT):
            return {"cefr_level": None, "cefr_status": "insufficient_evidence"}

        hint = str(llm_hint or "").upper().strip()
        if hint in {"A1", "A2", "B1", "B2", "C1", "C2"}:
            return {
                "cefr_level": hint,
                "cefr_status": "experimental_llm_hint_not_calibrated",
            }
        return {"cefr_level": None, "cefr_status": "not_calibrated"}
