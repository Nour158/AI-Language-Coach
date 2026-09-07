from sentence_transformers import CrossEncoder


class Reranker:
    """
    Reranks retrieved chunks using a CrossEncoder.

    Input:
        Query + hybrid retrieval results

    Output:
        The most relevant chunks ordered by reranker score
    """

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L6-v2",
        top_k=5,
    ):
        self.top_k = top_k

        print(f"Loading reranker: {model_name}")

        self.model = CrossEncoder(model_name)

    def rerank(self, query, results):
        if not results:
            return []

        pairs = [
            [query, result["text"]]
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked_results = []

        for result, score in zip(results, scores):
            reranked_result = result.copy()
            reranked_result["reranker_score"] = float(score)

            reranked_results.append(reranked_result)

        reranked_results.sort(
            key=lambda item: item["reranker_score"],
            reverse=True,
        )

        return reranked_results[:self.top_k]