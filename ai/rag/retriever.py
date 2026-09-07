from collections import defaultdict

from qdrant_client.models import SparseVector

from ai.rag.embeddings import BGEEmbeddings
from ai.rag.sparse_embeddings import SparseEmbeddings
from ai.rag.vector_store import QdrantVectorStore


class HybridRetriever:
    def __init__(
        self,
        collection_name="language_coach",
        initial_top_k=10,
        final_top_k=10,
        rrf_k=60,
    ):
        self.initial_top_k = initial_top_k
        self.final_top_k = final_top_k
        self.rrf_k = rrf_k

        print("Loading dense embeddings...")
        self.dense_model = BGEEmbeddings()

        print("Loading sparse embeddings...")
        self.sparse_model = SparseEmbeddings()

        self.vector_store = QdrantVectorStore(
            collection_name=collection_name
        )

    def _dense_search(self, query):
        dense_vector = self.dense_model.embed_query(query)

        results = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection_name,
            query=dense_vector,
            using="dense",
            limit=self.initial_top_k,
            with_payload=True,
        ).points

        return results

    def _sparse_search(self, query):
        sparse_embedding = self.sparse_model.embed_query(query)

        sparse_vector = SparseVector(
            indices=sparse_embedding.indices.tolist(),
            values=sparse_embedding.values.tolist(),
        )

        results = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection_name,
            query=sparse_vector,
            using="sparse",
            limit=self.initial_top_k,
            with_payload=True,
        ).points

        return results

    def _rrf_fusion(self, dense_results, sparse_results):
        scores = defaultdict(float)
        result_map = {}

        for rank, result in enumerate(dense_results, start=1):
            point_id = str(result.id)

            scores[point_id] += 1 / (self.rrf_k + rank)
            result_map[point_id] = result

        for rank, result in enumerate(sparse_results, start=1):
            point_id = str(result.id)

            scores[point_id] += 1 / (self.rrf_k + rank)
            result_map[point_id] = result

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )

        fused_results = []

        for point_id in ranked_ids[:self.final_top_k]:
            result = result_map[point_id]
            payload = result.payload or {}

            fused_results.append({
                "id": point_id,
                "rrf_score": scores[point_id],
                "text": payload.get("text", ""),
                "metadata": {
                    key: value
                    for key, value in payload.items()
                    if key != "text"
                },
            })

        return fused_results

    def retrieve(self, query):
        dense_results = self._dense_search(query)
        sparse_results = self._sparse_search(query)

        return self._rrf_fusion(
            dense_results,
            sparse_results,
        )

    def close(self):
        self.vector_store.close()