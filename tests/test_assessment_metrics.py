from evaluation.assessment_metrics import evaluate_numeric_scores, evaluate_cefr, issue_detection_prf

def test_numeric_metrics():
    result = evaluate_numeric_scores([70, 80], [60, 90])
    assert result["mae"] == 10.0

def test_cefr_accuracy():
    result = evaluate_cefr(["B1", "A2"], ["B1", "B1"])
    assert result["accuracy"] == 0.5

def test_issue_prf():
    result = issue_detection_prf(
        [["verb_form", "article"]],
        [["verb_form", "preposition"]],
    )
    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
    assert result["f1"] == 0.5
