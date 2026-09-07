from ai.rag.document_loader import KnowledgeDocumentLoader


loader = KnowledgeDocumentLoader("data/knowledge")

documents = loader.load_all()

print("\n===== DOCUMENT LOADER TEST =====")
print("Total documents loaded:", len(documents))

print("\nFirst 5 documents:")
for i, doc in enumerate(documents[:5], start=1):
    print(f"\n--- Document {i} ---")
    print("Metadata:", doc["metadata"])
    print("Text preview:", doc["text"][:200])