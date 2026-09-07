from ai.rag.retriever import HybridRetriever


retriever = HybridRetriever(
    initial_top_k=10,
    final_top_k=10,
)

query = "When should I use the present perfect tense?"

print("\n===== QUERY =====")
print(query)

results = retriever.retrieve(query)

print("\n===== HYBRID RRF RESULTS =====")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("RRF Score:", result["rrf_score"])
    print("Metadata:", result["metadata"])
    print("Text:")
    print(result["text"][:500])

retriever.close()