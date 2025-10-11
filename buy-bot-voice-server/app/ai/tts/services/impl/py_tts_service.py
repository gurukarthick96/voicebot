import pyttsx3
from typing_extensions import override

from app.ai.tts.services import TTSService
from app.utils import singleton, post_init


@singleton
@post_init
class PyTTSService(TTSService):

    @override
    def __init__(self, voice_name: str, rate: int = 150, volume: float = 1.0):
        super().__init__()

        self.voice_name = voice_name
        self.rate = rate
        self.volume = volume

    @override
    def __post_init__(self):
        super().__post_init__()

        self.engine = pyttsx3.init()

        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        self._set_voice()

    def _set_voice(self):
        voices = self.engine.getProperty('voices')
        selected = next((voice for voice in voices if self.voice_name == voice.name), None)
        if selected:
            self.engine.setProperty('voice', selected.id)

    @override
    def speak(self, texts: list[str]) -> None:
        self.engine.say(' '.join(texts))
        self.engine.runAndWait()

    @override
    def synthesize(self, texts: list[str]) -> str:
        raise NotImplementedError()


py_tts_service = PyTTSService('Microsoft Zira Desktop - English (United States)')

__all__ = ['py_tts_service']
