from app.ai.llm.models import LLMItem, LLMGroup
from app.base.converters import ConverterRegistry
from app.core.models import Item, Group
from app.order.models import LineItem, LineItemGroup


class LLMGroupConverter(ConverterRegistry[LLMGroup]):
    @staticmethod
    @ConverterRegistry.register(LineItemGroup)
    def _to_line_item_groups(llm_groups: list[LLMGroup], *, groups: list[Group]) -> list[LineItemGroup]:
        name_to_group = {group.name: group for group in groups}

        return [
            LLMGroupConverter._to_line_item_group(llm_group, matched_group)
            for llm_group in llm_groups
            if (matched_group := name_to_group.get(llm_group.name))
        ]

    @staticmethod
    def _to_line_item_group(llm_group: LLMGroup, group: Group) -> LineItemGroup:
        name_to_modifier = {modifier.name: modifier for modifier in group.items}

        modifiers = [
            LineItem.from_item(item, 1)
            for modifier_name in llm_group.modifiers
            if (item := name_to_modifier.get(modifier_name))
        ]

        return LineItemGroup.from_group(group, modifiers)


class LLMItemConverter(ConverterRegistry[LLMItem]):
    @staticmethod
    @ConverterRegistry.register(LineItem)
    def _to_line_items(llm_items: list[LLMItem], *, items: list[Item]) -> list[LineItem]:
        name_to_item = {item.name: item for item in items}

        return [
            LLMItemConverter._to_line_item(llm_item, item)
            for llm_item in llm_items
            if llm_item.quantity > 0
            if (item := name_to_item.get(llm_item.name))
        ]

    @staticmethod
    def _to_line_item(llm_item: LLMItem, item: Item) -> LineItem:
        groups = LLMGroupConverter(llm_item.groups).convert(LineItemGroup, groups=item.groups)

        return LineItem.from_item(item, llm_item.quantity, groups)


__all__ = ['LLMItemConverter']
