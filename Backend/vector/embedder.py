from typing import List

from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """
    Wrapper around sentence-transformers so we have a single place
    to load the model and control normalization.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model = SentenceTransformer(model_name)

    @property
    def dimension(self) -> int:
        """Return the underlying model's embedding dimension."""
        return int(self._model.get_sentence_embedding_dimension())

    def embed_text(self, text: str) -> List[float]:
        """Encode a single piece of text into a vector."""
        embedding = self._model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Encode a batch of texts into vectors."""
        if not texts:
            return []
        embeddings = self._model.encode(texts, normalize_embeddings=True)
        return [e.tolist() for e in embeddings]


_embedder: LocalEmbedder | None = None


def get_embedder() -> LocalEmbedder:
    """Singleton accessor for the local embedder."""
    global _embedder
    if _embedder is None:
        _embedder = LocalEmbedder()
    return _embedder

