REPORT_SCHEMA_VERSION = "1.0"
DIMENSIONS = (
    "grammar", "vocabulary", "fluency_naturalness",
    "coherence", "sentence_structure", "repeated_mistakes",
)

def clamp_score(value, default=0.0):
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = float(default)
    return round(max(0.0, min(100.0, value)), 2)

def mistake_schema(original, corrected, natural_alternative, category, explanation,
                   severity="medium", source="detector"):
    return {
        "original": str(original).strip(),
        "corrected": str(corrected).strip(),
        "natural_alternative": str(natural_alternative).strip(),
        "category": str(category or "other").strip().lower().replace(" ", "_"),
        "explanation": str(explanation).strip(),
        "severity": severity if severity in {"low", "medium", "high"} else "medium",
        "source": str(source),
    }

def empty_report():
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "overall_score": 0.0,
        "cefr_level": None,
        "cefr_status": "insufficient_evidence",
        "scoring_status": "experimental_heuristic_not_calibrated",
        "scores": {d: 0.0 for d in DIMENSIONS},
        "strengths": [],
        "weaknesses": [],
        "mistakes": [],
        "repeated_patterns": [],
        "exercises": [],
        "summary": "Not enough learner language was provided for assessment.",
        "metadata": {
            "learner_turns": 0,
            "learner_words": 0,
            "assistant_messages_scored": 0,
            "llm_used": False,
            "fluency_mode": "text_only_proxy",
        },
    }

def validate_report(report):
    required = {
        "schema_version", "overall_score", "cefr_level", "cefr_status",
        "scoring_status", "scores", "strengths", "weaknesses", "mistakes",
        "repeated_patterns", "exercises", "summary", "metadata",
    }
    missing = required - set(report)
    if missing:
        raise ValueError(f"Missing report fields: {sorted(missing)}")
    if set(DIMENSIONS) - set(report["scores"]):
        raise ValueError("Missing assessment dimension scores.")
    for mistake in report["mistakes"]:
        for key in ("original", "corrected", "natural_alternative", "category", "explanation"):
            if key not in mistake:
                raise ValueError(f"Mistake missing field: {key}")
