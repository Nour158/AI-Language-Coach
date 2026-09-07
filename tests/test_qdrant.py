from ai.rag.vector_store import QdrantVectorStore


store = QdrantVectorStore()

try:
    store.create_collection()
    print("Qdrant test finished.")
finally:
    store.client.close()