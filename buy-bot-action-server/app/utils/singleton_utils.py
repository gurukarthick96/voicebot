import threading
from functools import wraps


def singleton(cls):
    instance = None
    lock = threading.Lock()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        with lock:
            if instance is not None:
                raise RuntimeError(f'{cls.__name__} is a singleton and has already been instantiated.')
            instance = cls(*args, **kwargs)
            return instance

    return wrapper


__all_ = ['singleton']
