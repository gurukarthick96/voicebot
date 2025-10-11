from typing import Optional

from qdrant_client.http.models import ScoredPoint

from app.ai.nlp import DescriptiveKeywordExtractor, keyword_extractor
from app.core.models import Item
from app.core.services import ItemService, item_service
from app.utils import singleton
from app.vector.dao import ItemVectorDao, item_vector_dao
from app.vector.enums import ItemVectorName


@singleton
class ItemVectorService:

    def __init__(self,
                 item_service: ItemService,
                 item_vector_dao: ItemVectorDao,
                 keyword_extractor: DescriptiveKeywordExtractor,
                 vector_limit=3):
        self.item_service = item_service
        self.item_vector_dao = item_vector_dao
        self.keyword_extractor = keyword_extractor
        self.vector_limit = vector_limit

    def find_qualified_items(self, user_input: str) -> list[Item]:
        return self._find_qualified_items(ItemVectorName.FULL, user_input, score_threshold=0.3)

    def find_qualified_items_by_ids(self, user_input: str, item_ids: list[str]) -> list[Item]:
        return self._find_qualified_items(ItemVectorName.ITEM, user_input, score_threshold=0.5, item_ids=item_ids)

    def _find_qualified_items(
            self,
            vector_name: ItemVectorName,
            user_input: str,
            *,
            score_threshold: float,
            item_ids: Optional[list[str]] = None,
    ) -> list[Item]:
        item_keywords = self._extract_keywords(user_input)

        scored_points = self._search_items(vector_name, item_keywords, item_ids=item_ids)

        return self._get_high_confidence_items(scored_points, score_threshold)

    def _extract_keywords(self, user_input: str) -> str:
        return self.keyword_extractor.extract(user_input)

    def _search_items(
            self,
            vector_name: ItemVectorName,
            item_keywords: str,
            *,
            item_ids: Optional[list[str]] = None
    ) -> list[ScoredPoint]:
        if item_ids:
            return self.item_vector_dao.search_by_ids(vector_name, item_keywords, self.vector_limit, item_ids)
        else:
            return self.item_vector_dao.search(vector_name, item_keywords, self.vector_limit)

    def _get_high_confidence_items(self, scored_points: list[ScoredPoint], score_threshold: float) -> list[Item]:
        return [
            self.item_service.get_by_id(item_id)
            for point in scored_points
            if point.score >= score_threshold
            if (item_id := point.payload.get('id'))
        ]


item_vector_service = ItemVectorService(item_service, item_vector_dao, keyword_extractor)

__all__ = ['ItemVectorService', 'item_vector_service']
