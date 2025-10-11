from fastembed import TextEmbedding
from numpy import ndarray
from qdrant_client.fastembed_common import SUPPORTED_EMBEDDING_MODELS
from qdrant_client.http.models import Distance

from app import config
from app.utils import singleton


@singleton
class TextEmbedder:

    def __init__(self, model_name: str):
        self.model = TextEmbedding(model_name)

        self.size, self.distance = self._get_model_params(model_name)

    def embed(self, text: str) -> ndarray:
        return self.embed_all([text])[0]

    def embed_all(self, texts: list[str]) -> list[ndarray]:
        return list(self.model.embed(texts))

    @classmethod
    def _get_model_params(cls, model_name: str) -> tuple[int, Distance]:
        return SUPPORTED_EMBEDDING_MODELS[model_name]


text_embedder = TextEmbedder(config.TEXT_EMBEDDING_MODEL_NAME)

__all__ = ['TextEmbedder', 'text_embedder']
