from collections import Counter
from .utils import tokenize

FUNCTION_WORDS = {
    "the","a","an","and","or","but","to","of","in","on","at","for","with",
    "is","am","are","was","were","be","i","you","he","she","it","we","they",
    "my","your","this","that","do","does","did","have","has","had"
}

class VocabularyAnalyzer:
    def analyze(self, text):
        words = tokenize(text)
        if not words:
            return {"score": 0.0, "strengths": [], "weaknesses": ["No learner vocabulary was available."],
                    "evidence": {}, "confidence": "low"}

        unique = set(words)
        content = [w for w in words if w not in FUNCTION_WORDS]
        content_unique = set(content)
        counts = Counter(content)
        ttr = len(unique) / len(words)
        content_ttr = len(content_unique) / max(len(content), 1)
        repeated = [w for w, count in counts.most_common() if count >= 3][:8]

        diversity = ((ttr + content_ttr) / 2) * 100
        sample_factor = min(1.0, len(words) / 100)
        score = (45 + (diversity - 40) * 0.72) * (0.72 + 0.28 * sample_factor)
        score = max(30, min(94, score))

        return {
            "score": round(score, 2),
            "strengths": ["The learner shows useful lexical variety in the session."]
                         if len(words) >= 35 and content_ttr >= 0.62 else [],
            "weaknesses": ["Some content words are overused: " + ", ".join(repeated[:5])]
                          if repeated else [],
            "evidence": {
                "word_count": len(words),
                "unique_word_count": len(unique),
                "type_token_ratio": round(ttr, 3),
                "content_type_token_ratio": round(content_ttr, 3),
                "repeated_content_words": repeated,
            },
            "confidence": "medium" if len(words) >= 30 else "low",
        }
