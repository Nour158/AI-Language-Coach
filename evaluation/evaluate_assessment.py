import argparse
import json
import math
from pathlib import Path
from ai.assessment.session_evaluator import evaluate_session

def _mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0

def mae(predictions, references):
    return _mean(abs(float(p) - float(r)) for p, r in zip(predictions, references))

def rmse(predictions, references):
    return math.sqrt(_mean((float(p) - float(r)) ** 2 for p, r in zip(predictions, references)))

def accuracy(predictions, references):
    pairs = list(zip(predictions, references))
    return sum(str(p) == str(r) for p, r in pairs) / len(pairs) if pairs else 0.0

def evaluate_records(records):
    score_predictions, score_references = [], []
    cefr_predictions, cefr_references = [], []

    for record in records:
        history = record.get("conversation_history") or record.get("conversation") or []
        report = evaluate_session(history)

        if isinstance(record.get("overall_score"), (int, float)):
            score_predictions.append(report["overall_score"])
            score_references.append(record["overall_score"])

        if record.get("cefr_level"):
            cefr_predictions.append(report.get("cefr_level"))
            cefr_references.append(record["cefr_level"])

    result = {
        "records": len(records),
        "score_metrics": None,
        "cefr_metrics": None,
        "note": "Metrics are meaningful only with valid assessment-dataset or expert reference labels.",
    }

    if score_references:
        result["score_metrics"] = {
            "mae": round(mae(score_predictions, score_references), 4),
            "rmse": round(rmse(score_predictions, score_references), 4),
            "count": len(score_references),
        }

    if cefr_references:
        pairs = [(p, r) for p, r in zip(cefr_predictions, cefr_references) if p is not None]
        result["cefr_metrics"] = {
            "accuracy": round(
                accuracy([p for p, _ in pairs], [r for _, r in pairs]), 4
            ) if pairs else 0.0,
            "defensible_prediction_count": len(pairs),
            "reference_count": len(cefr_references),
        }

    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    path = Path(args.input)

    if path.suffix.lower() == ".jsonl":
        records = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    else:
        records = json.loads(path.read_text(encoding="utf-8"))

    print(json.dumps(evaluate_records(records), indent=2))

if __name__ == "__main__":
    main()
