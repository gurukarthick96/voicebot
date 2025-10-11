from abc import ABC, abstractmethod

from app.ai.genai.configs import ConfigType


class AbstractGenAIService(ABC):

    @abstractmethod
    def generate_text(self, input_text: str, config_type: ConfigType, temperature: float = None) -> str:
        pass


__all__ = ['AbstractGenAIService']
