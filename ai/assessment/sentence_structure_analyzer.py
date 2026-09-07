from .utils import sentence_split, tokenize

SUBORDINATORS = {
    "because","although","while","when","if","unless","before","after",
    "since","that","which","who"
}

class SentenceStructureAnalyzer:
    def analyze(self, text):
        sentences = sentence_split(text)
        if not sentences:
            return {"score": 0.0, "strengths": [], "weaknesses": ["No learner sentences were available."],
                    "evidence": {}, "confidence": "low"}

        lengths = [len(tokenize(s)) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        short_ratio = sum(x <= 5 for x in lengths) / len(lengths)
        complex_count = sum(bool(set(tokenize(s)) & SUBORDINATORS) for s in sentences)
        complex_ratio = complex_count / len(sentences)
        variety = min(1.0, len(set(lengths)) / max(3, len(sentences)))

        score = 58 + complex_ratio * 18 + variety * 14
        if 7 <= avg_len <= 18:
            score += 5
        if short_ratio > 0.75 and len(sentences) >= 4:
            score -= 8

        strengths = ["The learner uses some subordinate clauses and varied sentence forms."]                     if complex_ratio >= 0.25 else []
        weaknesses = []
        if short_ratio > 0.75 and len(sentences) >= 4:
            weaknesses.append("Many sentences are very short; combining related ideas could improve structure.")
        if complex_ratio < 0.10 and len(sentences) >= 5:
            weaknesses.append("Sentence patterns are mostly simple; more clause variety may help.")

        return {
            "score": round(max(30, min(95, score)), 2),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "evidence": {
                "sentence_count": len(sentences),
                "average_sentence_words": round(avg_len, 2),
                "short_sentence_ratio": round(short_ratio, 3),
                "complex_sentence_ratio": round(complex_ratio, 3),
            },
            "confidence": "medium" if len(sentences) >= 4 else "low",
        }
