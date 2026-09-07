from ai.assessment.session_evaluator import SessionEvaluator
from ai.assessment.proficiency_scorer import ProficiencyScorer
from ai.assessment.schemas import validate_report
from ai.feedback.feedback_pipeline import FeedbackPipeline

def test_only_learner_messages_are_scored():
    evaluator = SessionEvaluator(use_llm=False)
    a = evaluator.evaluate([{"role": "user", "content": "I have went home."}])
    b = evaluator.evaluate([
        {"role": "assistant", "content": "She are more better."},
        {"role": "user", "content": "I have went home."},
    ])
    assert a["scores"]["grammar"] == b["scores"]["grammar"]
    assert b["metadata"]["assistant_messages_scored"] == 0

def test_mistake_schema_and_repeated_pattern():
    evaluator = SessionEvaluator(use_llm=False)
    report = evaluator.evaluate([
        {"role": "user", "content": "I have went there. I have went home."}
    ])
    required = {"original", "corrected", "natural_alternative", "category", "explanation"}
    assert required.issubset(report["mistakes"][0])
    assert report["repeated_patterns"][0]["category"] == "verb_form"

def test_cefr_is_not_fabricated_from_score_thresholds():
    scorer = ProficiencyScorer()
    assert scorer.cefr_result(20, 1, "B2")["cefr_level"] is None
    result = scorer.cefr_result(100, 4, "B1")
    assert result["cefr_level"] == "B1"
    assert "experimental" in result["cefr_status"]

def test_stable_report_schema():
    evaluator = SessionEvaluator(use_llm=False)
    report = evaluator.evaluate([
        {"role": "user", "content": "I enjoy English because it helps me travel."},
        {"role": "user", "content": "Although it is difficult, I keep studying."},
        {"role": "user", "content": "I want to become more confident when I speak."},
    ])
    validate_report(report)
    assert "sentence_structure" in report["scores"]
    assert report["scoring_status"] == "experimental_heuristic_not_calibrated"

def test_exercises_use_observed_weakness():
    pipeline = FeedbackPipeline()
    result = pipeline.process(
        mistakes=[{
            "original": "I have went.",
            "corrected": "I have gone.",
            "natural_alternative": "I've gone.",
            "category": "verb_form",
            "explanation": "Use a past participle.",
        }],
        repeated_patterns=[{
            "category": "verb_form", "count": 2, "examples": [], "priority": "medium"
        }],
        strengths=[],
        weaknesses=["Verb forms need review."],
    )
    assert result["exercises"][0]["based_on_observed_weakness"] == "verb_form"
