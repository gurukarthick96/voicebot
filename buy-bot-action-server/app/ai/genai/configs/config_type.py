from enum import Enum

from app.ai.genai.configs import ConfigMeta
from app.ai.llm.models import LLMMenu
from app.ai.llm.prompts.system_instructions import MENU_ITEM_EXTRACTION_INSTRUCTION


class ConfigType(Enum):
    MENU_ITEM_EXTRACTION = ConfigMeta(
        system_instruction=MENU_ITEM_EXTRACTION_INSTRUCTION,
        response_mime_type='application/json',
        response_schema=LLMMenu
    )


__all__ = ['ConfigType']
