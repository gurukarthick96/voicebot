from app.ai.llm.models import LLMMenu
from app.base.converters.llm import LLMItemConverter
from app.core.models import Item
from app.order.models import LineItem


def build_line_item_response(input_items: list[Item], output_text: str) -> list[LineItem]:
    llm_menu = LLMMenu.model_validate_json(output_text)

    llm_items = [llm_item for llm_item in llm_menu.root if llm_item.quantity > 0]

    return LLMItemConverter(llm_items).convert(LineItem, items=input_items)


__all__ = ['build_line_item_response']
