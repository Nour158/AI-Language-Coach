from __future__ import annotations
import math
import re
from collections import Counter

def safe_mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0

def normalize_text(text):
    text = re.sub(r"\s+", " ", str(text or "").strip().lower())
    return text

def exact_match(prediction, reference):
    return float(normalize_text(prediction) == normalize_text(reference))

def token_f1(prediction, reference):
    pred = normalize_text(prediction).split()
    ref = normalize_text(reference).split()
    if not pred and not ref:
        return 1.0
    if not pred or not ref:
        return 0.0

    overlap = sum((Counter(pred) & Counter(ref)).values())
    precision = overlap / len(pred)
    recall = overlap / len(ref)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0

def mae(predictions, references):
    pairs = [(float(p), float(r)) for p, r in zip(predictions, references)]
    return safe_mean(abs(p - r) for p, r in pairs)

def rmse(predictions, references):
    pairs = [(float(p), float(r)) for p, r in zip(predictions, references)]
    return math.sqrt(safe_mean((p - r) ** 2 for p, r in pairs))

def pearson_correlation(predictions, references):
    xs = [float(x) for x in predictions]
    ys = [float(y) for y in references]
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    mx, my = safe_mean(xs), safe_mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (dx * dy) if dx and dy else 0.0

def accuracy(predictions, references):
    pairs = list(zip(predictions, references))
    if not pairs:
        return 0.0
    return sum(str(p) == str(r) for p, r in pairs) / len(pairs)
