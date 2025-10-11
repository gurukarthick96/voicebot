from typing import TypeVar, Iterable, Callable

T = TypeVar('T')


def find_first_by_predicate(iterable: Iterable[T], predicate: Callable[[T], bool], default=None) -> T:
    return next((i for i in iterable if predicate(i)), default)


def find_all_by_predicate(iterable: Iterable[T], predicate: Callable[[T], bool]) -> list[T]:
    return list(filter(predicate, iterable))


def replace_one_by_key_fn(source_iterable: Iterable[T],
                          target: T,
                          key_fn: Callable[[T], any]
                          ) -> list[T]:
    return [
        target if key_fn(source) == key_fn(target) else source for source in source_iterable
    ]


def replace_all_by_key_fn(source_iterable: Iterable[T],
                          target_iterable: Iterable[T],
                          key_fn: Callable[[T], any]
                          ) -> list[T]:
    target_map = {key_fn(target): target for target in target_iterable}

    return [
        target_map.get(key_fn(source), source) for source in source_iterable
    ]


__all__ = ['find_first_by_predicate', 'find_all_by_predicate', 'replace_one_by_key_fn', 'replace_all_by_key_fn']
