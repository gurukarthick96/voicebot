import io
from contextlib import contextmanager


@contextmanager
def bytes_buffer(input_bytes: bytes = None):
    buffer = io.BytesIO(input_bytes) if input_bytes else io.BytesIO()

    try:
        yield buffer
    finally:
        buffer.close()


__all__ = ['bytes_buffer']
