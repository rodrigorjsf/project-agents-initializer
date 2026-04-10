"""Fastembed multi-model wrapper with lazy loading."""

from __future__ import annotations

from fastembed import TextEmbedding


class Embedder:
    """Manages multiple embedding models with lazy initialization."""

    def __init__(self, cache_dir: str = ".rag/models") -> None:
        self.cache_dir = cache_dir
        self._models: dict[str, TextEmbedding] = {}

    def _get_model(self, model_name: str) -> TextEmbedding:
        if model_name not in self._models:
            self._models[model_name] = TextEmbedding(
                model_name=model_name,
                cache_dir=self.cache_dir,
                lazy_load=True,
            )
        return self._models[model_name]

    def embed_texts(
        self, texts: list[str], model_name: str, batch_size: int = 256
    ) -> list[list[float]]:
        """Embed document texts for indexing.

        Uses embed() which applies document-side encoding.
        Returns list of float lists (one per input text).
        """
        if not texts:
            return []
        model = self._get_model(model_name)
        # embed() returns a generator of NDArray[float32] — must materialize
        embeddings = list(model.embed(texts, batch_size=batch_size))
        return [e.tolist() for e in embeddings]

    def embed_query(self, query: str, model_name: str) -> list[float]:
        """Embed a search query.

        Uses query_embed() for asymmetric encoding (e.g., bge models
        prepend a query instruction prefix for better retrieval).
        """
        model = self._get_model(model_name)
        # query_embed() returns a generator — materialize and take first
        embeddings = list(model.query_embed(query))
        return embeddings[0].tolist()
