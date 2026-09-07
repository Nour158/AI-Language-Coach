from evaluation.rag_metrics import hit_rate_at_k, recall_at_k, mean_reciprocal_rank

def test_rag_metrics():
    retrieved = [["a", "b", "c"], ["x", "y"]]
    relevant = [["b"], ["z"]]
    assert hit_rate_at_k(retrieved, relevant, 2) == 0.5
    assert recall_at_k(retrieved, relevant, 2) == 0.5
    assert mean_reciprocal_rank(retrieved, relevant) == 0.25
