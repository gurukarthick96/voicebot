from typing import Type, TypeVar, Callable, Generic

S = TypeVar('S')
T = TypeVar('T')


class ConverterRegistry(Generic[S]):
    _registry: dict[type, Callable[[list[S], ...], list]] = {}

    def __init__(self, source: list[S]):
        self.source = source

    @classmethod
    def register(cls, target_type: Type[T]):
        def decorator(func: Callable[..., list[T]]):
            cls._registry[target_type] = func
            return func

        return decorator

    def convert(self, target_type: Type[T], **kwargs) -> list[T]:
        func = self._registry.get(target_type)
        if func is None:
            raise ValueError(f'no function registered for target conversion: {target_type}')

        return func(self.source, **kwargs)


__all__ = ['ConverterRegistry']
