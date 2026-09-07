from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    SparseVectorParams,
)

from ai.config import VECTOR_DB_DIR


class QdrantVectorStore:
    def __init__(self, collection_name="language_coach"):
        self.collection_name = collection_name

        self.client = QdrantClient(
            path=str(VECTOR_DB_DIR)
        )

    def create_collection(
        self,
        vector_size=768,
        recreate=False,
    ):
        collections = self.client.get_collections().collections

        existing_names = [
            collection.name
            for collection in collections
        ]

        if self.collection_name in existing_names:
            if recreate:
                self.client.delete_collection(
                    collection_name=self.collection_name
                )
                print("Old collection deleted.")
            else:
                print("Collection already exists.")
                return

        self.client.create_collection(
            collection_name=self.collection_name,

            vectors_config={
                "dense": VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                )
            },

            sparse_vectors_config={
                "sparse": SparseVectorParams()
            },
        )

        print("Collection created.")

    def close(self):
        self.client.close()