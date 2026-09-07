from __future__ import annotations
from typing import Any, Callable, Dict, Iterable, List, Optional

from .conversation_metrics import aggregate_conversation_quality, reference_similarity
from .grammar_correction_metrics import evaluate_corrections
from .assessment_metrics import evaluate_numeric_scores, evaluate_cefr, issue_detection_prf
from .rag_metrics import hit_rate_at_k, recall_at_k, mean_reciprocal_rank

class EvaluationRunner:
    def evaluate_conversation(
        self,
        records: Iterable[Dict[str, Any]],
        generate_fn: Callable[[str, list], Dict[str, Any] | str],
    ) -> Dict[str, Any]:
        responses = []
        references = []

        for record in records:
            prompt = record.get("input_text", "")
            history = record.get("conversation", [])
            result = generate_fn(prompt, history)

            if isinstance(result, dict):
                response = result.get("response", "")
            else:
                response = str(result)

            responses.append(response)
            if record.get("target_text"):
                references.append(record["target_text"])

        report = aggregate_conversation_quality(responses)
        if references and len(references) == len(responses):
            report["reference_token_f1"] = round(reference_similarity(responses, references), 4)
        return report

    def evaluate_grammar_correction(
        self,
        records: Iterable[Dict[str, Any]],
        correct_fn: Callable[[str], str],
    ) -> Dict[str, Any]:
        predictions, references = [], []
        for record in records:
            if not record.get("target_text"):
                continue
            predictions.append(correct_fn(record.get("input_text", "")))
            references.append(record["target_text"])
        return evaluate_corrections(predictions, references)

    def evaluate_assessment(
        self,
        records: Iterable[Dict[str, Any]],
        assess_fn: Callable[[list], Dict[str, Any]],
        score_key: str = "overall_score",
    ) -> Dict[str, Any]:
        score_predictions, score_references = [], []
        cefr_predictions, cefr_references = [], []
        predicted_issues, reference_issues = [], []

        for record in records:
            history = record.get("conversation") or [
                {"role": "user", "content": record.get("input_text", "")}
            ]
            result = assess_fn(history)

            label = record.get("label")
            if isinstance(label, (int, float)):
                score_predictions.append(result.get(score_key, 0))
                score_references.append(label)
            elif isinstance(label, str) and label.upper() in {"A1","A2","B1","B2","C1","C2"}:
                cefr_predictions.append(result.get("estimated_cefr", "Insufficient evidence"))
                cefr_references.append(label.upper())

            ref_issue_types = record.get("metadata", {}).get("issue_types")
            if ref_issue_types:
                pred_issue_types = [
                    x.get("type")
                    for x in result.get("repeated_mistakes", [])
                    if isinstance(x, dict)
                ]
                predicted_issues.append(pred_issue_types)
                reference_issues.append(ref_issue_types)

        report = {}
        if score_references:
            report["score_metrics"] = evaluate_numeric_scores(score_predictions, score_references)
        if cefr_references:
            report["cefr_metrics"] = evaluate_cefr(cefr_predictions, cefr_references)
        if reference_issues:
            report["issue_detection"] = issue_detection_prf(predicted_issues, reference_issues)
        return report

    def evaluate_rag(
        self,
        queries: List[str],
        relevant_lists: List[list],
        retrieve_fn: Callable[[str], list],
        k_values=(3, 5, 10),
    ) -> Dict[str, Any]:
        retrieved_lists = [retrieve_fn(query) for query in queries]

        report = {"mrr": round(mean_reciprocal_rank(retrieved_lists, relevant_lists), 4)}
        for k in k_values:
            report[f"hit_rate@{k}"] = round(hit_rate_at_k(retrieved_lists, relevant_lists, k), 4)
            report[f"recall@{k}"] = round(recall_at_k(retrieved_lists, relevant_lists, k), 4)
        return report
