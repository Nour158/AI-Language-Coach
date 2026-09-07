from .utils import tokenize, sentence_split

FILLERS = {"um", "uh", "erm", "hmm", "like"}

class FluencyAnalyzer:
    def analyze(self, text, metadata=None):
        words = tokenize(text)
        sentences = sentence_split(text)
        filler_count = sum(1 for w in words if w in FILLERS)
        filler_rate = filler_count / max(len(words), 1)
        avg_sentence_words = len(words) / max(len(sentences), 1)

        duration = 0.0
        pauses = 0
        speech = False
        for item in metadata or []:
            try:
                if item.get("duration_seconds") is not None:
                    duration += float(item["duration_seconds"])
                    speech = True
                if item.get("pause_count") is not None:
                    pauses += int(item["pause_count"])
                    speech = True
            except (TypeError, ValueError):
                pass

        wpm = len(words) / (duration / 60) if speech and duration > 0 else None
        if wpm:
            penalty = min(18, max(0, 70 - wpm) * 0.25)
            penalty += min(15, max(0, wpm - 190) * 0.15)
            score = 88 - penalty - min(18, filler_rate * 200)
            mode, confidence = "speech_metadata_plus_text", "medium"
        else:
            score = 80 - min(20, filler_rate * 220)
            if len(words) >= 20 and avg_sentence_words < 4:
                score -= 7
            mode, confidence = "text_only_proxy", "low"

        weaknesses = []
        if filler_rate >= 0.08:
            weaknesses.append("Frequent fillers may reduce conversational smoothness.")
        if not speech:
            weaknesses.append("Spoken fluency cannot be fully judged from text alone.")

        return {
            "score": round(max(25, min(95, score)), 2),
            "strengths": ["The available sample contains little filler-word use."]
                         if len(words) >= 30 and filler_rate < 0.03 else [],
            "weaknesses": weaknesses,
            "evidence": {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "average_sentence_words": round(avg_sentence_words, 2),
                "filler_count": filler_count,
                "filler_rate": round(filler_rate, 3),
                "words_per_minute": round(wpm, 2) if wpm else None,
                "pause_count": pauses if speech else None,
                "mode": mode,
            },
            "confidence": confidence,
        }
