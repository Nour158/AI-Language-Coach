from fastembed import SparseTextEmbedding

SPARSE_MODEL_NAME = "prithivida/Splade_PP_en_v1"


class SparseEmbeddings:
    def __init__(self):
        print(f"Loading sparse embedding model: {SPARSE_MODEL_NAME}")

        self.model = SparseTextEmbedding(
            model_name=SPARSE_MODEL_NAME
        )

    def embed_documents(self, texts):
        return list(self.model.embed(texts))

    def embed_query(self, query):
        return list(self.model.query_embed(query))[0]