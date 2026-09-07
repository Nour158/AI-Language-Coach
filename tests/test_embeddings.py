from ai.rag.embeddings import BGEEmbeddings


embedder = BGEEmbeddings()

texts = [
    "The present perfect connects past actions to the present.",
    "The past simple describes completed actions in the past.",
    "Modal verbs include can, could, may, might, must and should."
]

document_vectors = embedder.embed_documents(texts)

query_vector = embedder.embed_query(
    "When should I use present perfect?"
)

print("Number of document vectors:", len(document_vectors))
print("Embedding dimension:", len(document_vectors[0]))
print("Query dimension:", len(query_vector))