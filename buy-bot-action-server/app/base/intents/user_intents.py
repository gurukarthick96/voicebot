from enum import Enum


class UserOrderIntent(Enum):
    pass


class UserCartIntent(UserOrderIntent):
    CHECKOUT = 'CHECKOUT'
    ADD_ITEMS = 'ADD_ITEMS'
    UPDATE_ITEMS = 'UPDATE_ITEMS'
    DELETE_ITEMS = 'DELETE_ITEMS'


__all__ = ['UserOrderIntent', 'UserCartIntent']
