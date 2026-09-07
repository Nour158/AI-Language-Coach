from ai.rag.retriever import HybridRetriever
from ai.rag.reranker import Reranker


query = "When should I use the present perfect tense?"


print("\n===== HYBRID RETRIEVAL =====")

retriever = HybridRetriever(
    initial_top_k=10,
    final_top_k=10,
)

hybrid_results = retriever.retrieve(query)

print(f"Hybrid candidates: {len(hybrid_results)}")


print("\n===== RERANKING =====")

reranker = Reranker(
    top_k=5
)

final_results = reranker.rerank(
    query,
    hybrid_results,
)


print("\n===== FINAL TOP 5 =====")

for i, result in enumerate(final_results, start=1):

    print(f"\n--- Result {i} ---")

    print(
        "Reranker Score:",
        result["reranker_score"],
    )

    print(
        "RRF Score:",
        result["rrf_score"],
    )

    print(
        "Metadata:",
        result["metadata"],
    )

    print("Text:")
    print(result["text"][:500])


retriever.close()