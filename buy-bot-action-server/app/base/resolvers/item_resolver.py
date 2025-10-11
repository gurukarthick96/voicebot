from typing import Optional

from typeguard import typechecked

from app.ai.llm.services import CoreLLMService, core_llm_service
from app.core.models import Item
from app.order.models import LineItem
from app.utils import singleton, find_all_by_predicate
from app.vector.services import ItemVectorService, item_vector_service


@singleton
@typechecked
class ItemResolver:

    def __init__(self,
                 item_vector_service: ItemVectorService,
                 core_llm_service: CoreLLMService):
        self.item_vector_service = item_vector_service
        self.core_llm_service = core_llm_service

    def resolve_new_line_items_using_llm(self, user_input: str) -> list[LineItem]:
        qualified_items = self._find_qualified_items(user_input)

        return self.core_llm_service.extract_line_item_details(qualified_items, user_input)

    def resolve_existing_line_items(self, user_input: str, line_items: list[LineItem]) -> list[LineItem]:
        item_ids = [line_item.item_id for line_item in line_items]

        qualified_items = self._find_qualified_items(user_input, item_ids)

        return self._filter_line_items_by_items(line_items, qualified_items)

    def resolve_existing_line_items_using_llm(self, user_input: str, line_items: list[LineItem]) -> list[LineItem]:
        item_ids = [line_item.item_id for line_item in line_items]

        qualified_items = self._find_qualified_items(user_input, item_ids)

        extracted_line_items = self.core_llm_service.extract_line_item_details(qualified_items, user_input)

        return self._replace_line_items_by_item_id(line_items, extracted_line_items)

    def _find_qualified_items(self, user_input: str, item_ids: Optional[list[str]] = None) -> list[Item]:
        if item_ids:
            qualified_items = self.item_vector_service.find_qualified_items_by_ids(user_input, item_ids)
        else:
            qualified_items = self.item_vector_service.find_qualified_items(user_input)

        if not qualified_items:
            raise ValueError('no qualified items found for the given user input.')

        return qualified_items

    @staticmethod
    def _filter_line_items_by_items(line_items: list[LineItem], items: list[Item]) -> list[LineItem]:
        item_ids = {item.id for item in items}

        return find_all_by_predicate(line_items, lambda line_item: line_item.item_id in item_ids)

    @staticmethod
    def _replace_line_items_by_item_id(source_list: list[LineItem], target_list: list[LineItem]) -> list[LineItem]:
        target_map = {item.item_id: item for item in target_list}

        def replace_with_target(source: LineItem) -> LineItem:
            target = target_map.get(source.item_id)
            if target:
                target.line_item_id = source.line_item_id
                return target
            return source

        return [replace_with_target(source) for source in source_list]


item_resolver = ItemResolver(item_vector_service, core_llm_service)

__all__ = ['ItemResolver', 'item_resolver']
