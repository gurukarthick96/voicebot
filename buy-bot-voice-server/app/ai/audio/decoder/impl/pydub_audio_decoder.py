import base64

from pydub import AudioSegment
from typing_extensions import override

from app.ai.audio.decoder import AudioDecoder
from app.utils import post_init, singleton, bytes_buffer


@singleton
@post_init
class PydubAudioDecoder(AudioDecoder):

    @override
    def __init__(self):
        super().__init__()

    @override
    def __post_init__(self):
        super().__post_init__()

    @override
    def _decode(self, encoded_audio: str) -> bytes:
        audio_bytes = base64.b64decode(encoded_audio)

        return self._convert_to_wav(audio_bytes)

    @staticmethod
    def _convert_to_wav(audio_bytes: bytes) -> bytes:
        with bytes_buffer(audio_bytes) as input_buffer:
            audio_segment = AudioSegment.from_file(input_buffer)
            return PydubAudioDecoder._export_to_bytes(audio_segment, 'wav')

    @staticmethod
    def _export_to_bytes(audio_segment: AudioSegment, format_type: str) -> bytes:
        with bytes_buffer() as output_buffer:
            audio_segment.export(output_buffer, format=format_type)
            return output_buffer.getvalue()


pydub_audio_decoder = PydubAudioDecoder()

__all__ = ['pydub_audio_decoder']
