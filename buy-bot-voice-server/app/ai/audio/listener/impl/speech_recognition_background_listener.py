import queue
import threading
from functools import cached_property
from typing import Optional, Callable

import speech_recognition as sr
from typing_extensions import override

from app.ai.audio.listener import AudioListener
from app.utils import post_init, singleton, logger


@singleton
@post_init
class SpeechRecognitionBackgroundListener(AudioListener):

    @override
    def __init__(self,
                 timeout: int = 10,
                 phrase_time_limit: int = None,
                 pause_threshold: float = 2.0):
        super().__init__()

        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.pause_threshold = pause_threshold

        # Thread management
        self._thread: Optional[threading.Thread] = None
        self._listen_event = threading.Event()
        self._stop_event = threading.Event()

        # Audio handling
        self._stop_listening_func: Optional[Callable] = None

    @override
    def __post_init__(self):
        super().__post_init__()

        self.audio_queue = queue.Queue()
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = self.pause_threshold

    @override
    @cached_property
    def source(self) -> sr.AudioSource:
        return sr.Microphone()

    @override
    def __enter__(self):
        self._ensure_thread_running()
        return self

    @override
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _ensure_thread_running(self):
        if self._thread is None or not self._thread.is_alive():
            if self._stop_event.is_set():
                self._stop_event.clear()
                self._listen_event.clear()

            self._thread = threading.Thread(
                target=self._run_listener,
                daemon=True,
                name="AudioListenerThread"
            )

            self._thread.start()

    def _run_listener(self):
        try:
            self._start_listening()
        except:
            logger.error('audio thread error', exc_info=True)
        finally:
            self._stop_listening()

    def _start_listening(self):
        self._clear_audio_queue()

        try:
            with self.source as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)

            self._stop_listening_func = self.recognizer.listen_in_background(
                self.source,
                self._audio_callback,
                phrase_time_limit=self.phrase_time_limit
            )

            self._listen_event.set()
            logger.info('🎙️ Listening started...')

            self._stop_event.wait()

        except:
            logger.error('unable to start listener', exc_info=True)
            raise

    def _stop_listening(self):
        self._listen_event.clear()

        if self._stop_listening_func:
            try:
                self._stop_listening_func(wait_for_stop=False)
                logger.info('🎙️ Listening stopped')
            except:
                logger.error(f'unable to stop listener', exc_info=True)
            finally:
                self._stop_listening_func = None

    def _audio_callback(self, recognizer: sr.Recognizer, audio: sr.AudioData):
        if not self._listen_event.is_set():
            return

        try:
            logger.info('🎙️ Audio captured, processing...')
            self.audio_queue.put_nowait(audio)
        except queue.Full:
            logger.error('audio queue full', exc_info=True)

    def _clear_audio_queue(self):
        try:
            while True:
                self.audio_queue.get_nowait()
        except queue.Empty:
            pass

    def stop(self):
        self._stop_event.set()

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3.0)

        self._thread = None

    @override
    def _listen(self) -> sr.AudioData:
        self._ensure_thread_running()

        if not self._listen_event.wait(timeout=3.0):
            raise RuntimeError('audio listener failed to start within timeout')

        try:
            return self.audio_queue.get(timeout=self.timeout)
        except queue.Empty:
            raise RuntimeError('no audio captured within timeout period')


speech_recognition_background_listener = SpeechRecognitionBackgroundListener(
    timeout=10, phrase_time_limit=30, pause_threshold=2.0
)

__all__ = ['speech_recognition_background_listener']
