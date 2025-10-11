from enum import Enum


class ItemVectorName(str, Enum):
    ITEM = 'item_vector'
    FULL = 'full_vector'


__all__ = ['ItemVectorName']
