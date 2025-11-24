from cachetools import TTLCache, cached
from google.genai import Client
from google.genai.types import GenerateContentConfig

from app import config
from app.ai.genai.configs import ConfigType, ConfigMeta
from app.ai.genai.services import AbstractGenAIService
from app.utils import singleton


@singleton
class GeminiService(AbstractGenAIService):

    def __init__(self, api_key: str, model_name: str):
        self.client = Client(api_key=api_key)
        self.model_name = model_name
        self.cache = TTLCache(maxsize=100, ttl=3600)

    @cached
    def generate_text(self, input_text: str, config_type: ConfigType, temperature: float = None) -> str:
        cache_key = (input_text, config_type, temperature)
        if cache_key in self.cache:
            return self.cache[cache_key]

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=input_text,
            config=self._build_config(config_type, temperature)
        )

        result = response.text
        self.cache[cache_key] = result
        return result

    def _build_config(self, config_type: ConfigType, temperature) -> GenerateContentConfig:
        config_meta: ConfigMeta = config_type.value

        return GenerateContentConfig(
            temperature=temperature,
            response_mime_type=config_meta.response_mime_type,
            system_instruction=config_meta.system_instruction,
            response_schema=config_meta.response_schema,
        )


gemini_service = GeminiService(config.GEMINI_API_KEY, config.GEMINI_MODEL_NAME)

__all__ = ['gemini_service']
