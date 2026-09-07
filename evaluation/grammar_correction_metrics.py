from __future__ import annotations
from .common_metrics import safe_mean, exact_match, token_f1

def evaluate_corrections(predictions, references):
    return {
        "exact_match": round(safe_mean(exact_match(p, r) for p, r in zip(predictions, references)), 4),
        "token_f1": round(safe_mean(token_f1(p, r) for p, r in zip(predictions, references)), 4),
        "count": len(list(zip(predictions, references))),
    }
