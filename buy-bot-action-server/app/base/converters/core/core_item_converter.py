from app.ai.llm.models import LLMItem, LLMGroup
from app.base.converters import ConverterRegistry
from app.core.models import Item, Group
from app.order.models import LineItem, LineItemGroup


class GroupConverter(ConverterRegistry[Group]):
    @staticmethod
    @ConverterRegistry.register(LLMGroup)
    def _to_llm_groups(groups: list[Group]) -> list[LLMGroup]:
        return [
            LLMGroup(name=group.name, modifiers=[modifier.name for modifier in group.items])
            for group in groups
        ]

    @staticmethod
    @ConverterRegistry.register(LineItemGroup)
    def _to_line_item_groups(groups: list[Group]) -> list[LineItemGroup]:
        ...


class ItemConverter(ConverterRegistry[Item]):
    @staticmethod
    @ConverterRegistry.register(LLMItem)
    def _to_llm_items(items: list[Item]) -> list[LLMItem]:
        return [
            LLMItem(name=item.name, groups=GroupConverter(item.groups).convert(LLMGroup))
            for item in items
        ]

    @staticmethod
    @ConverterRegistry.register(LineItem)
    def _to_line_items(items: list[Item]) -> list[LineItem]:
        ...


__all__ = ['ItemConverter']
