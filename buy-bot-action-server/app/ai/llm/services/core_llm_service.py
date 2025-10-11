from app.ai.genai.configs import ConfigType
from app.ai.genai.services import AbstractGenAIService, genai_service
from app.ai.llm.builders import build_llm_menu_and_user_input_content, build_line_item_response
from app.core.models import Item
from app.order.models import LineItem
from app.utils import singleton


@singleton
class CoreLLMService:

    def __init__(self, genai_service: AbstractGenAIService):
        self.genai_service = genai_service

    def extract_line_item_details(self, items: list[Item], user_input: str) -> list[LineItem]:
        content = build_llm_menu_and_user_input_content(items, user_input)

        response = self.genai_service.generate_text(content, ConfigType.MENU_ITEM_EXTRACTION)

        return build_line_item_response(items, response)


core_llm_service = CoreLLMService(genai_service)

__all__ = ['CoreLLMService', 'core_llm_service']
