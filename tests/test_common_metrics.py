from evaluation.common_metrics import exact_match, token_f1, mae, accuracy

def test_exact_match():
    assert exact_match("Hello world", " hello   world ") == 1.0

def test_token_f1():
    assert 0 < token_f1("I have a car", "I have car") <= 1.0

def test_mae():
    assert mae([70, 80], [60, 90]) == 10.0

def test_accuracy():
    assert accuracy(["B1", "A2"], ["B1", "B1"]) == 0.5
