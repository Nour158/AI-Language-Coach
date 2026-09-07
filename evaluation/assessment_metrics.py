from __future__ import annotations
from .common_metrics import accuracy, mae, rmse, pearson_correlation

def evaluate_numeric_scores(predictions, references):
    return {
        "mae": round(mae(predictions, references), 4),
        "rmse": round(rmse(predictions, references), 4),
        "pearson": round(pearson_correlation(predictions, references), 4),
    }

def evaluate_cefr(predictions, references):
    return {
        "accuracy": round(accuracy(predictions, references), 4),
        "count": len(list(zip(predictions, references))),
    }

def issue_detection_prf(predicted_issue_sets, reference_issue_sets):
    tp = fp = fn = 0
    for pred, ref in zip(predicted_issue_sets, reference_issue_sets):
        pred = set(pred)
        ref = set(ref)
        tp += len(pred & ref)
        fp += len(pred - ref)
        fn += len(ref - pred)

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }
