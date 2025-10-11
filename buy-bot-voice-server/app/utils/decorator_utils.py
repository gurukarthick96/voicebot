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
                raise RuntimeError(f'{cls.__name__} is a singleton and has already been instantiated')
            instance = cls(*args, **kwargs)
            return instance

    return wrapper


def post_init(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def wrapper(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if hasattr(self, '__post_init__'):
            self.__post_init__()
        else:
            raise RuntimeError('__post_init__ not defined')

    cls.__init__ = wrapper

    return cls


__all_ = ['singleton', 'post_init']
