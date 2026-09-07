from .grammar_analyzer import GrammarAnalyzer
from .vocabulary_analyzer import VocabularyAnalyzer
from .fluency_analyzer import FluencyAnalyzer
from .coherence_analyzer import CoherenceAnalyzer
from .sentence_structure_analyzer import SentenceStructureAnalyzer
from .mistake_tracker import MistakeTracker
from .proficiency_scorer import ProficiencyScorer
from .llm_assessor import LLMAssessor
from .schemas import REPORT_SCHEMA_VERSION, empty_report, validate_report
from .utils import learner_messages, join_text, tokenize, optional_metadata
from ai.feedback.feedback_pipeline import FeedbackPipeline

class SessionEvaluator:
    def __init__(self, llm_client=None, use_llm=True):
        self.grammar = GrammarAnalyzer()
        self.vocabulary = VocabularyAnalyzer()
        self.fluency = FluencyAnalyzer()
        self.coherence = CoherenceAnalyzer()
        self.structure = SentenceStructureAnalyzer()
        self.tracker = MistakeTracker()
        self.scorer = ProficiencyScorer()
        self.feedback = FeedbackPipeline()
        self.llm = LLMAssessor(llm_client) if use_llm else None

    @staticmethod
    def _unique(items):
        output = []
        for item in items:
            if item and item not in output:
                output.append(item)
        return output

    def evaluate(self, conversation_history):
        learner = learner_messages(conversation_history)
        if not learner:
            return empty_report()

        text = join_text(learner)
        word_count = len(tokenize(text))
        metadata = optional_metadata(learner)

        grammar = self.grammar.analyze(text)
        heuristic = {
            "grammar": grammar,
            "vocabulary": self.vocabulary.analyze(text),
            "fluency_naturalness": self.fluency.analyze(text, metadata),
            "coherence": self.coherence.analyze(learner),
            "sentence_structure": self.structure.analyze(text),
        }

        llm_result = {}
        llm_used = False
        llm_error = None
        if self.llm and self.llm.available():
            try:
                llm_result = self.llm.assess(learner)
                llm_used = True
            except Exception as exc:
                llm_error = str(exc)

        mistakes = list(grammar.get("mistakes", []))
        if llm_used:
            seen = {(m.get("original"), m.get("category")) for m in mistakes}
            for item in llm_result.get("mistakes", []):
                signature = (item.get("original"), item.get("category"))
                if signature not in seen:
                    mistakes.append(item)
                    seen.add(signature)

        repeated_patterns = self.tracker.track(mistakes)
        repeated_analysis = self.tracker.analyze(mistakes, repeated_patterns)

        scores, strengths, weaknesses = {}, [], []
        for dimension in ("grammar", "vocabulary", "fluency_naturalness", "coherence", "sentence_structure"):
            llm_score = llm_result.get("scores", {}).get(dimension) if llm_used else None
            scores[dimension] = self.scorer.blend_dimension(
                heuristic[dimension]["score"], llm_score
            )
            strengths += heuristic[dimension].get("strengths", [])
            weaknesses += heuristic[dimension].get("weaknesses", [])

        scores["repeated_mistakes"] = repeated_analysis["score"]
        strengths += repeated_analysis.get("strengths", [])
        weaknesses += repeated_analysis.get("weaknesses", [])

        if llm_used:
            strengths += llm_result.get("strengths", [])
            weaknesses += llm_result.get("weaknesses", [])

        strengths = self._unique(strengths)[:8]
        weaknesses = self._unique(weaknesses)[:8]

        feedback = self.feedback.process(
            mistakes[:12], repeated_patterns, strengths, weaknesses
        )

        cefr = self.scorer.cefr_result(
            learner_words=word_count,
            learner_turns=len(learner),
            llm_hint=llm_result.get("cefr_hint") if llm_used else None,
        )

        summary = str(llm_result.get("summary", "")).strip() if llm_used else ""
        if not summary:
            strongest = max(scores, key=scores.get)
            weakest = min(scores, key=scores.get)
            summary = (
                f"The strongest measured area is {strongest.replace('_', ' ')}. "
                f"The main area to prioritize is {weakest.replace('_', ' ')}. "
                "Scores are experimental heuristics until validated against assessment data."
            )

        report = {
            "schema_version": REPORT_SCHEMA_VERSION,
            "overall_score": self.scorer.overall(scores),
            "cefr_level": cefr["cefr_level"],
            "cefr_status": cefr["cefr_status"],
            "scoring_status": "experimental_heuristic_not_calibrated",
            "scores": scores,
            "strengths": feedback["strengths"],
            "weaknesses": feedback["weaknesses"],
            "mistakes": feedback["mistakes"],
            "repeated_patterns": repeated_patterns,
            "exercises": feedback["exercises"],
            "summary": summary,
            "metadata": {
                "learner_turns": len(learner),
                "learner_words": word_count,
                "assistant_messages_scored": 0,
                "llm_used": llm_used,
                "llm_error": llm_error,
                "fluency_mode": heuristic["fluency_naturalness"]["evidence"].get(
                    "mode", "text_only_proxy"
                ),
            },
        }
        validate_report(report)
        return report

_service = None

def get_session_evaluator():
    global _service
    if _service is None:
        _service = SessionEvaluator()
    return _service

def evaluate_session(conversation_history):
    if not isinstance(conversation_history, list):
        raise TypeError("conversation_history must be a list of role/content messages.")
    return get_session_evaluator().evaluate(conversation_history)
