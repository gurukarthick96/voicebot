from __future__ import annotations

from typing import Callable, Generic, TypeVar, Any

from app.base.intents import UserOrderIntent
from app.order.facades import OrderFacade
from app.order.models import Order

T = TypeVar('T', bound=UserOrderIntent)


class OrderIntentHandlerRegistry(Generic[T]):
    _registry: dict[type, Callable[[OrderIntentHandlerRegistry, str, OrderFacade], None]] = {}

    @classmethod
    def register(cls, user_intent: T):
        def decorator(func: Callable[[OrderIntentHandlerRegistry, str, OrderFacade], None]):
            cls._registry[user_intent] = func
            return func

        return decorator

    def handle(self, user_intent: T, user_input: str, order_dict: dict[str, Any]) -> Order:
        func = self._registry.get(user_intent)
        if func is None:
            raise ValueError(f'no function registered for intent: {user_intent}')

        order_facade = OrderFacade.from_dict(order_dict)

        func(self, user_input, order_facade)

        return order_facade.order


__all__ = ['OrderIntentHandlerRegistry']
