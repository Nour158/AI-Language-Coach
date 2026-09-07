from ai.rag.retriever import DenseRetriever


retriever = DenseRetriever(top_k=5)

query = "When should I use the present perfect tense?"

print("\n===== QUERY =====")
print(query)

results = retriever.retrieve(query)

print("\n===== TOP RESULTS =====")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Score:", result["score"])
    print("Metadata:", result["metadata"])
    print("Text:")
    print(result["text"][:500])

retriever.close()