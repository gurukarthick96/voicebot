import sounddevice as sd
from TTS.api import TTS
from typing_extensions import override

from app.ai.tts.services import TTSService
from app.utils import singleton, post_init


@singleton
@post_init
class CoquiTTSService(TTSService):

    @override
    def __init__(self, model_name: str):
        super().__init__()

        self.model_name = model_name

    @override
    def __post_init__(self):
        super().__post_init__()

        self.tts = TTS(model_name=self.model_name)
        self.sampling_rate = self.tts.synthesizer.output_sample_rate

    @override
    def speak(self, texts: list[str]) -> None:
        audio = self.tts.tts(text=' '.join(texts))

        sd.play(audio, samplerate=self.sampling_rate)
        sd.wait()

    @override
    def synthesize(self, texts: list[str]) -> str:
        raise NotImplementedError()


coqui_tts_service = CoquiTTSService(model_name="tts_models/en/ljspeech/glow-tts")

__all__ = ['coqui_tts_service']
