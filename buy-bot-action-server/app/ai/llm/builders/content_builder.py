from app.ai.llm.models import LLMItem, LLMMenu
from app.ai.llm.prompts import build_menu_and_user_input_prompt
from app.base.converters.core import ItemConverter
from app.core.models import Item


def build_llm_menu_and_user_input_content(items: list[Item], user_input: str) -> str:
    llm_items = ItemConverter(items).convert(LLMItem)

    llm_menu = LLMMenu(root=llm_items)

    return build_menu_and_user_input_prompt(llm_menu.model_dump_json(), user_input)


__all__ = ['build_llm_menu_and_user_input_content']
