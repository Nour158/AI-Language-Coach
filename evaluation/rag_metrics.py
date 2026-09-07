from __future__ import annotations
from .common_metrics import safe_mean

def _id(item):
    if isinstance(item, dict):
        return (
            item.get("id")
            or item.get("chunk_id")
            or item.get("source")
            or item.get("text")
        )
    return item

def hit_rate_at_k(retrieved_lists, relevant_lists, k=5):
    scores = []
    for retrieved, relevant in zip(retrieved_lists, relevant_lists):
        rel = {_id(x) for x in relevant}
        top = {_id(x) for x in retrieved[:k]}
        scores.append(float(bool(rel & top)))
    return safe_mean(scores)

def recall_at_k(retrieved_lists, relevant_lists, k=5):
    scores = []
    for retrieved, relevant in zip(retrieved_lists, relevant_lists):
        rel = {_id(x) for x in relevant}
        if not rel:
            continue
        top = {_id(x) for x in retrieved[:k]}
        scores.append(len(rel & top) / len(rel))
    return safe_mean(scores)

def reciprocal_rank(retrieved, relevant):
    rel = {_id(x) for x in relevant}
    for rank, item in enumerate(retrieved, start=1):
        if _id(item) in rel:
            return 1.0 / rank
    return 0.0

def mean_reciprocal_rank(retrieved_lists, relevant_lists):
    return safe_mean(
        reciprocal_rank(retrieved, relevant)
        for retrieved, relevant in zip(retrieved_lists, relevant_lists)
    )

def source_diversity(retrieved):
    sources = []
    for item in retrieved:
        if isinstance(item, dict):
            source = item.get("source") or item.get("metadata", {}).get("source")
            if source:
                sources.append(source)
    return len(set(sources)) / len(sources) if sources else 0.0
