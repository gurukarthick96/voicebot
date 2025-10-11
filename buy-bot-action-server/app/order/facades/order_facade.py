from __future__ import annotations

from typing import Optional

from typeguard import typechecked

from app.order.models import Order, LineItem, Discount, Payment
from app.order.services import OrderService, order_service


@typechecked
class OrderFacade:

    def __init__(self, order_service: OrderService, order: Optional[Order] = None):
        self.order_service = order_service
        self.order = order or self.order_service.create_order()

    @classmethod
    def from_dict(cls, order_dict: Optional[dict] = None) -> OrderFacade:
        order = Order.from_dict(order_dict) if order_dict else None

        return OrderFacade(order_service, order)

    def get_order(self) -> Order:
        return self.order

    def add_line_item(self, line_item: LineItem) -> OrderFacade:
        self.order = self.order_service.add_line_item(self.order, line_item)

        return self

    def add_line_items(self, line_items: list[LineItem]) -> OrderFacade:
        self.order = self.order_service.add_line_items(self.order, line_items)

        return self

    def update_line_item(self, line_item: LineItem) -> OrderFacade:
        self.order = self.order_service.update_line_item(self.order, line_item)

        return self

    def update_line_items(self, line_items: list[LineItem]) -> OrderFacade:
        self.order = self.order_service.update_line_items(self.order, line_items)

        return self

    def remove_line_item(self, line_item_id: str) -> OrderFacade:
        self.order = self.order_service.remove_line_item(self.order, line_item_id)

        return self

    def remove_line_items(self, line_item_ids: list[str]) -> OrderFacade:
        self.order = self.order_service.remove_line_items(self.order, line_item_ids)

        return self

    def update_line_item_quantity(self, line_item_id: str, quantity: int) -> OrderFacade:
        self.order = self.order_service.update_line_item_quantity(self.order, line_item_id, quantity)

        return self

    def update_line_item_modifier_quantity(self, line_item_id: str,
                                           line_item_modifier_id: str, quantity: int) -> OrderFacade:
        self.order = self.order_service.update_line_item_modifier_quantity(self.order, line_item_id,
                                                                           line_item_modifier_id, quantity)

        return self

    def add_discount(self, discount: Discount) -> OrderFacade:
        self.order = self.order_service.add_discount(self.order, discount)

        return self

    def remove_discount(self, discount_id: str) -> OrderFacade:
        self.order = self.order_service.remove_discount(self.order, discount_id)

        return self

    def add_payment(self, payment: Payment) -> OrderFacade:
        self.order = self.order_service.add_payment(self.order, payment)

        return self

    def remove_payment(self, payment_id: str) -> OrderFacade:
        self.order = self.order_service.remove_payment(self.order, payment_id)

        return self


__all__ = ['OrderFacade']
