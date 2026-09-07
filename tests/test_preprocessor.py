from collections import Counter

from ai.rag.document_loader import KnowledgeDocumentLoader
from ai.rag.preprocessor import KnowledgePreprocessor


# 1. Load all knowledge documents
loader = KnowledgeDocumentLoader("data/knowledge")
documents = loader.load_all()

# 2. Preprocess and chunk them
preprocessor = KnowledgePreprocessor(
    chunk_size=1200,
    overlap=150
)

chunks = preprocessor.process_documents(documents)

# 3. Basic counts
print("\n===== PREPROCESSOR TEST =====")
print("Raw documents:", len(documents))
print("Total chunks:", len(chunks))

# 4. Count chunks by knowledge category
category_counts = Counter(
    chunk["metadata"].get("category", "unknown")
    for chunk in chunks
)

print("\n===== CHUNKS BY CATEGORY =====")

for category, count in category_counts.items():
    print(f"{category}: {count}")

# 5. Show first 5 chunks
print("\n===== FIRST 5 CHUNKS =====")

for i, chunk in enumerate(chunks[:5], start=1):
    print(f"\n--- Chunk {i} ---")
    print("Metadata:", chunk["metadata"])
    print("Text preview:", chunk["text"][:300])

# 6. Check some vocabulary chunks specifically
vocabulary_chunks = [
    chunk
    for chunk in chunks
    if chunk["metadata"].get("category") == "vocabulary"
]

print("\n===== VOCABULARY CHECK =====")
print("Vocabulary chunks:", len(vocabulary_chunks))

for i, chunk in enumerate(vocabulary_chunks[:3], start=1):
    print(f"\n--- Vocabulary Chunk {i} ---")
    print("Metadata:", chunk["metadata"])
    print("Text preview:", chunk["text"][:300])