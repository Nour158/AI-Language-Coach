import json
import re
from .schemas import mistake_schema, clamp_score

class LLMAssessor:
    def __init__(self, client=None):
        self.client = client or self._load_client()

    @staticmethod
    def _load_client():
        try:
            from ai.llm.qwen_client import QwenClient
            return QwenClient()
        except Exception:
            return None

    def available(self):
        return self.client is not None

    def assess(self, messages):
        if not self.client:
            raise RuntimeError("Qwen client unavailable.")

        transcript = "\n".join(
            "Learner: " + str(m.get("content", ""))
            for m in messages if m.get("content")
        )
        prompt = (
            "Assess ONLY the learner English after the completed session. "
            "Never score assistant English. Do not invent errors. "
            "Do not claim scientifically calibrated CEFR. "
            "Return JSON only with keys: scores containing grammar, vocabulary, "
            "fluency_naturalness, coherence, sentence_structure; strengths; weaknesses; "
            "mistakes containing original, corrected, natural_alternative, category, "
            "explanation, severity; cefr_hint; summary.\n\nLEARNER TRANSCRIPT:\n"
            + transcript
        )

        raw = self.client.generate(prompt, max_new_tokens=1100)
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", (raw or "").strip(), flags=re.I)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            start, end = cleaned.find("{"), cleaned.rfind("}")
            if start < 0 or end <= start:
                raise ValueError("LLM did not return valid JSON.")
            data = json.loads(cleaned[start:end + 1])

        dims = ("grammar", "vocabulary", "fluency_naturalness", "coherence", "sentence_structure")
        scores = {d: clamp_score((data.get("scores") or {}).get(d, 0)) for d in dims}
        mistakes = []
        for item in (data.get("mistakes") or [])[:12]:
            if isinstance(item, dict):
                mistakes.append(mistake_schema(
                    item.get("original", ""), item.get("corrected", ""),
                    item.get("natural_alternative", ""), item.get("category", "other"),
                    item.get("explanation", ""), item.get("severity", "medium"), "llm"
                ))
        return {
            "scores": scores,
            "strengths": [str(x) for x in (data.get("strengths") or [])][:8],
            "weaknesses": [str(x) for x in (data.get("weaknesses") or [])][:8],
            "mistakes": mistakes,
            "cefr_hint": data.get("cefr_hint"),
            "summary": str(data.get("summary", "")).strip(),
        }
