import re
from .schemas import mistake_schema
from .utils import sentence_split, tokenize

RULES = [
    (re.compile(r"\b(I|you|we|they)\s+is\b", re.I),
     "subject_verb_agreement", "Use am/are with this subject.", "high"),
    (re.compile(r"\b(he|she|it)\s+are\b", re.I),
     "subject_verb_agreement", "Use is with he, she, or it.", "high"),
    (re.compile(r"\b(have|has)\s+went\b", re.I),
     "verb_form", "After have/has, use the past participle 'gone'.", "high"),
    (re.compile(r"\bdid\s+\w+ed\b", re.I),
     "verb_form", "After did, use the base verb form.", "medium"),
    (re.compile(r"\bmore\s+\w+er\b", re.I),
     "comparative", "Avoid double comparatives such as 'more easier'.", "medium"),
]

def _correct(sentence, category):
    result = sentence
    if category == "subject_verb_agreement":
        result = re.sub(r"\bI\s+is\b", "I am", result, flags=re.I)
        result = re.sub(r"\b(you|we|they)\s+is\b",
                        lambda m: f"{m.group(1)} are", result, flags=re.I)
        result = re.sub(r"\b(he|she|it)\s+are\b",
                        lambda m: f"{m.group(1)} is", result, flags=re.I)
    if category == "verb_form":
        result = re.sub(r"\b(have|has)\s+went\b",
                        lambda m: f"{m.group(1)} gone", result, flags=re.I)
    return result

class GrammarAnalyzer:
    def detect(self, text):
        mistakes = []
        for sentence in sentence_split(text):
            for pattern, category, explanation, severity in RULES:
                if pattern.search(sentence):
                    corrected = _correct(sentence, category)
                    mistakes.append(mistake_schema(
                        sentence, corrected, corrected, category,
                        explanation, severity, "grammar_rule"
                    ))
        return mistakes

    def analyze(self, text):
        mistakes = self.detect(text)
        words = tokenize(text)
        error_rate = len(mistakes) / max(len(words), 1) * 100
        score = max(35.0, 94.0 - error_rate * 5.0)
        if len(words) < 12:
            score = min(score, 78.0)
        return {
            "score": round(score, 2),
            "strengths": ["No high-confidence grammar-rule errors were detected."]
                         if len(words) >= 25 and not mistakes else [],
            "weaknesses": ["Some grammar patterns need review."] if mistakes else [],
            "mistakes": mistakes,
            "evidence": {
                "word_count": len(words),
                "detected_mistakes": len(mistakes),
                "mistakes_per_100_words": round(error_rate, 2),
            },
            "confidence": "medium" if len(words) >= 25 else "low",
        }
