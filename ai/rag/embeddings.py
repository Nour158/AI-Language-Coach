from sentence_transformers import SentenceTransformer

from ai.config import EMBEDDING_MODEL_NAME


class BGEEmbeddings:
    """
    Wrapper for the BGE embedding model.

    Converts text into dense numerical vectors for semantic retrieval.
    """

    def __init__(self):
        print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")

        self.model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

    def embed_documents(self, texts):
        """
        Convert a list of documents/chunks into dense vectors.
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings.tolist()

    def embed_query(self, query):
        """
        Convert one search query into a dense vector.
        """

        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        return embedding.tolist()