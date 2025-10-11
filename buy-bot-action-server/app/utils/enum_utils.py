from enum import Enum
from typing import Type, TypeVar

T = TypeVar('T', bound=Enum)


def to_enum(enum_class: Type[T], value: str) -> T:
    try:
        return enum_class[value]
    except KeyError:
        raise NotImplementedError(f'unsupported enum value: {value}')


__all__ = ['to_enum']
