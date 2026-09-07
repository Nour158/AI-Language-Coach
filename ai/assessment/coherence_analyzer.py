from .utils import tokenize, sentence_split

CONNECTORS = {
    "because","so","but","however","although","therefore","then","first",
    "second","finally","also","instead","while","when","after","before"
}

class CoherenceAnalyzer:
    def analyze(self, messages):
        texts = [str(m.get("content", "")).strip() for m in messages if m.get("content")]
        text = " ".join(texts)
        words = tokenize(text)
        sentences = sentence_split(text)
        lower = text.lower()
        connectors = sum(lower.count(c) for c in CONNECTORS)

        turn_sets = [set(tokenize(t)) for t in texts]
        overlaps = []
        for a, b in zip(turn_sets, turn_sets[1:]):
            union = a | b
            overlaps.append(len(a & b) / len(union) if union else 0.0)
        overlap = sum(overlaps) / len(overlaps) if overlaps else 0.0

        score = 66 + min(16, connectors / max(len(sentences), 1) * 9)
        if len(texts) >= 2:
            score += min(9, overlap * 45)
        if len(words) >= 45:
            score += 4

        return {
            "score": round(min(94, score), 2),
            "strengths": ["The learner uses linking language to connect ideas."]
                         if connectors >= 2 else [],
            "weaknesses": ["Some learner turns have weak continuity with preceding ideas."]
                          if len(texts) >= 3 and overlap < 0.015 else [],
            "evidence": {
                "learner_turns": len(texts),
                "sentence_count": len(sentences),
                "connector_count": connectors,
                "adjacent_turn_overlap": round(overlap, 3),
            },
            "confidence": "medium" if len(texts) >= 3 and len(words) >= 35 else "low",
        }
