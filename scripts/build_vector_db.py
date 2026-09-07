from uuid import uuid5, NAMESPACE_URL

from qdrant_client.models import (
    PointStruct,
    SparseVector,
)

from ai.rag.document_loader import KnowledgeDocumentLoader
from ai.rag.preprocessor import KnowledgePreprocessor
from ai.rag.embeddings import BGEEmbeddings
from ai.rag.sparse_embeddings import SparseEmbeddings
from ai.rag.vector_store import QdrantVectorStore


BATCH_SIZE = 64


def build_vector_db():
    print("\n===== BUILDING HYBRID VECTOR DATABASE =====")

    print("\n[1/6] Loading knowledge files...")

    loader = KnowledgeDocumentLoader("data/knowledge")
    documents = loader.load_all()

    print(f"Loaded raw documents: {len(documents)}")

    print("\n[2/6] Preprocessing and chunking...")

    preprocessor = KnowledgePreprocessor(
        chunk_size=1200,
        overlap=150,
    )

    chunks = preprocessor.process_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    print("\n[3/6] Loading dense BGE model...")

    dense_model = BGEEmbeddings()

    print("\n[4/6] Loading sparse SPLADE model...")

    sparse_model = SparseEmbeddings()

    print("\n[5/6] Creating hybrid Qdrant collection...")

    vector_store = QdrantVectorStore(
        collection_name="language_coach"
    )

    vector_store.create_collection(
        vector_size=768,
        recreate=True,
    )

    print("\n[6/6] Creating dense + sparse vectors...")

    total_chunks = len(chunks)

    for start in range(0, total_chunks, BATCH_SIZE):

        end = min(
            start + BATCH_SIZE,
            total_chunks,
        )

        batch = chunks[start:end]

        texts = [
            chunk["text"]
            for chunk in batch
        ]

        dense_vectors = dense_model.embed_documents(texts)

        sparse_vectors = sparse_model.embed_documents(texts)

        points = []

        for chunk, dense_vector, sparse_vector in zip(
            batch,
            dense_vectors,
            sparse_vectors,
        ):

            payload = {
                "text": chunk["text"],
                **chunk["metadata"],
            }

            unique_key = (
                f"{chunk['metadata'].get('source', '')}"
                f"|{chunk['metadata'].get('page', '')}"
                f"|{chunk['metadata'].get('row', '')}"
                f"|{chunk['metadata'].get('chunk_index', '')}"
                f"|{chunk['text']}"
            )

            point_id = str(
                uuid5(
                    NAMESPACE_URL,
                    unique_key,
                )
            )

            point = PointStruct(
                id=point_id,

                vector={
                    "dense": dense_vector,

                    "sparse": SparseVector(
                        indices=sparse_vector.indices.tolist(),
                        values=sparse_vector.values.tolist(),
                    ),
                },

                payload=payload,
            )

            points.append(point)

        vector_store.client.upsert(
            collection_name=vector_store.collection_name,
            points=points,
        )

        progress = end / total_chunks * 100

        print(
            f"Uploaded {end}/{total_chunks} "
            f"({progress:.1f}%)"
        )

    print("\n===== HYBRID VECTOR DATABASE COMPLETE =====")
    print(f"Collection: {vector_store.collection_name}")
    print(f"Total chunks indexed: {total_chunks}")

    vector_store.close()


if __name__ == "__main__":
    build_vector_db()