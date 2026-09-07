from collections import Counter, defaultdict
from .config import REPEATED_PATTERN_THRESHOLD

class MistakeTracker:
    def track(self, mistakes):
        counts = Counter()
        examples = defaultdict(list)
        for item in mistakes or []:
            category = str(item.get("category", "other")).lower().replace(" ", "_")
            counts[category] += 1
            original = str(item.get("original", "")).strip()
            if original and original not in examples[category] and len(examples[category]) < 3:
                examples[category].append(original)

        return [
            {
                "category": category,
                "count": count,
                "examples": examples[category],
                "priority": "high" if count >= 4 else "medium",
            }
            for category, count in counts.most_common()
            if count >= REPEATED_PATTERN_THRESHOLD
        ]

    def analyze(self, mistakes, patterns):
        mistakes = list(mistakes or [])
        repeated_occurrences = sum(p["count"] for p in patterns)
        score = max(35, 94 - min(50, len(mistakes) * 3 + repeated_occurrences * 4))
        return {
            "score": round(score, 2),
            "strengths": ["No repeated high-confidence mistake pattern was detected."]
                         if not patterns else [],
            "weaknesses": ["Some error categories repeat across the session."]
                          if patterns else [],
            "evidence": {
                "total_detected_mistakes": len(mistakes),
                "repeated_pattern_count": len(patterns),
                "repeated_occurrences": repeated_occurrences,
            },
            "confidence": "medium",
        }
