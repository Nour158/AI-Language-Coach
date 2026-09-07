from evaluation.benchmark_runner import EvaluationRunner

def test_conversation_runner():
    runner = EvaluationRunner()
    report = runner.evaluate_conversation(
        [{"input_text": "Hi", "conversation": [], "target_text": ""}],
        lambda prompt, history: {"response": "Hi! How are you?"},
    )
    assert report["count"] == 1
    assert report["follow_up_question_rate"] == 1.0

def test_rag_runner():
    runner = EvaluationRunner()
    report = runner.evaluate_rag(
        queries=["q"],
        relevant_lists=[["a"]],
        retrieve_fn=lambda q: ["a", "b"],
        k_values=(1,),
    )
    assert report["hit_rate@1"] == 1.0
    assert report["recall@1"] == 1.0
