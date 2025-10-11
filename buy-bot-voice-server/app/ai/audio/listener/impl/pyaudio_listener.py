import math
import statistics
import time
from contextlib import contextmanager
from functools import cached_property

import pyaudio
import speech_recognition as sr
import webrtcvad
from typing_extensions import override

from app.ai.audio.listener import AudioListener
from app.utils import singleton, post_init, logger


@singleton
@post_init
class PyAudioListener(AudioListener):

    @override
    def __init__(self,
                 timeout: int = 10,
                 pause_threshold: float = 2.0):
        super().__init__()

        self.timeout = timeout
        self.pause_threshold = pause_threshold

        self.RATE = 16000
        self.FRAME_DURATION = 30  # ms
        self.FRAME_SIZE = int(self.RATE * self.FRAME_DURATION / 1000)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.DEFAULT_NOISE_THRESHOLD = 5.0

    @override
    def __post_init__(self):
        super().__post_init__()

        self.vad = webrtcvad.Vad(2)
        self.noise_threshold = self.calibrate_noise_level()
        self.sample_size = self.source.get_sample_size(self.FORMAT)

    @override
    @cached_property
    def source(self) -> pyaudio.PyAudio:
        return pyaudio.PyAudio()

    @contextmanager
    def _audio_stream(self):
        stream = self.source.open(
            rate=self.RATE,
            channels=self.CHANNELS,
            format=self.FORMAT,
            input=True,
            input_device_index=None,
            frames_per_buffer=self.FRAME_SIZE,
        )
        try:
            yield stream
        finally:
            stream.stop_stream()
            stream.close()

    @staticmethod
    def _rms_energy(frame):
        shorts = memoryview(frame).cast('h')
        return math.sqrt(sum(s ** 2 for s in shorts) / len(shorts)) if shorts else 0

    def calibrate_noise_level(self, duration=0.5) -> float:
        energies = []
        frames_to_read = int(self.RATE / self.FRAME_SIZE * duration)

        with self._audio_stream() as stream:
            for _ in range(frames_to_read):
                frame = stream.read(self.FRAME_SIZE, exception_on_overflow=False)
                energies.append(self._rms_energy(frame))

        if not energies:
            return self.DEFAULT_NOISE_THRESHOLD

        avg = statistics.mean(energies)
        std = statistics.stdev(energies) if len(energies) > 1 else 0
        noise_threshold = max(avg + std, self.DEFAULT_NOISE_THRESHOLD)

        logger.info('calibrated noise threshold: %.2f', noise_threshold)

        return noise_threshold

    def _is_speech(self, frame):
        return (self._rms_energy(frame) > self.noise_threshold) and self.vad.is_speech(frame, self.RATE)

    @override
    def _listen(self) -> sr.AudioData:
        frames = []

        start_time = time.time()
        pause_time = None
        speech_triggered = False

        logger.info('🎙️ Listening started...')
        with self._audio_stream() as stream:
            while True:
                frame = stream.read(self.FRAME_SIZE, exception_on_overflow=False)

                if self._is_speech(frame):
                    if not speech_triggered:
                        logger.info('🎙️ Speech started...')
                        speech_triggered = True
                    pause_time = None
                    frames.append(frame)
                else:
                    if not speech_triggered:
                        if time.time() - start_time > self.timeout:
                            break
                    else:
                        frames.append(frame)
                        if pause_time is None:
                            pause_time = time.time()
                        elif time.time() - pause_time > self.pause_threshold:
                            logger.info('🎙️ Speech ended.')
                            break

        if not frames:
            raise RuntimeError('timeout while listening')

        return sr.AudioData(
            b''.join(frames),
            self.RATE,
            self.sample_size
        )

    @override
    def cleanup(self):
        self.source.terminate()


pyaudio_listener = PyAudioListener(timeout=10, pause_threshold=1.5)

__all__ = ['pyaudio_listener']
