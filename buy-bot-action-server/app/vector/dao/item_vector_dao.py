from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchAny
from qdrant_client.http.models import VectorParams, PointStruct, ScoredPoint
from typeguard import typechecked

from app.ai.nlp import TextEmbedder, text_embedder
from app.utils import singleton, text_to_uuid
from app.vector import vector_db_client
from app.vector.domains import ItemVectorDomain
from app.vector.enums import ItemVectorName


@singleton
@typechecked
class ItemVectorDao:

    def __init__(self,
                 client: QdrantClient,
                 embedder: TextEmbedder,
                 collection_name='Item-Points'):
        self.client = client
        self.embedder = embedder
        self.collection_name = collection_name

        self.ensure_collection_exists()

    def ensure_collection_exists(self):
        if not self.client.collection_exists(self.collection_name):
            vector_param = VectorParams(size=self.embedder.size, distance=self.embedder.distance)

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    ItemVectorName.ITEM: vector_param,
                    ItemVectorName.FULL: vector_param,
                }
            )

    def upsert(self, vector_domains: list[ItemVectorDomain]):
        item_points = [self._build_point(domain) for domain in vector_domains]
        self.client.upsert(collection_name=self.collection_name, points=item_points)

    def search(self, vector_name: ItemVectorName, text: str, limit: int) -> list[ScoredPoint]:
        return self._search(vector_name, text, limit=limit)

    def search_by_ids(
            self, vector_name: ItemVectorName, text: str, limit: int, ids: list[str]
    ) -> list[ScoredPoint]:
        return self._search(vector_name, text, limit=limit, ids=ids)

    def _embed(self, text: str) -> list:
        return self.embedder.embed(text).tolist()

    def _build_point(self, domain: ItemVectorDomain) -> PointStruct:
        return PointStruct(
            id=text_to_uuid(domain.id),
            vector={
                ItemVectorName.ITEM: self._embed(domain.name),
                ItemVectorName.FULL: self._embed(domain.full_text),
            },
            payload=domain.model_dump()
        )

    def _search(
            self,
            vector_name: ItemVectorName,
            search_text: str,
            *,
            limit: int = 1,
            ids: Optional[list[str]] = None,
    ) -> list[ScoredPoint]:
        vector = self._embed(search_text)

        conditions = []
        # conditions.append(FieldCondition(key='tenant', match=MatchValue(value='DEFAULT')))
        # conditions.append(FieldCondition(key='context', match=MatchValue(value='DEFAULT')))
        if ids:
            conditions.append(FieldCondition(key='id', match=MatchAny(any=ids)))

        query_filter = Filter(must=conditions) if conditions else None

        query_response = self.client.query_points(
            collection_name=self.collection_name,
            using=vector_name,
            query=vector,
            query_filter=query_filter,
            limit=limit,
        )

        return query_response.points


item_vector_dao = ItemVectorDao(vector_db_client, text_embedder)

__all__ = ['ItemVectorDao', 'item_vector_dao']
