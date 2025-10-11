from __future__ import annotations

from typeguard import typechecked

from app.order.models import Order, LineItem, Discount, Payment
from app.utils import singleton, find_first_by_predicate, find_all_by_predicate, replace_all_by_key_fn, \
    replace_one_by_key_fn


@singleton
@typechecked
class OrderService:
    def create_order(self) -> Order:
        return Order()

    def add_line_item(self, order: Order, line_item: LineItem) -> Order:
        order.line_items.append(line_item)

        return order

    def add_line_items(self, order: Order, line_items: list[LineItem]) -> Order:
        order.line_items.extend(line_items)

        return order

    def update_line_item(self, order: Order, line_item: LineItem) -> Order:
        order.line_items = replace_one_by_key_fn(order.line_items, line_item,
                                                 lambda li: li.line_item_id)

        return order

    def update_line_items(self, order: Order, line_items: list[LineItem]) -> Order:
        order.line_items = replace_all_by_key_fn(order.line_items, line_items,
                                                 lambda li: li.line_item_id)

        return order

    def remove_line_item(self, order: Order, line_item_id: str) -> Order:
        order.line_items = find_all_by_predicate(order.line_items,
                                                 lambda line_item: line_item.line_item_id != line_item_id)

        return order

    def remove_line_items(self, order: Order, line_item_ids: list[str]) -> Order:
        order.line_items = find_all_by_predicate(order.line_items,
                                                 lambda line_item: line_item.line_item_id not in line_item_ids)

        return order

    def update_line_item_quantity(self, order: Order, line_item_id: str, quantity: int) -> Order:
        line_item = self._find_line_item_by_id(order.line_items, line_item_id)

        if line_item:
            line_item.quantity = quantity

        return order

    def update_line_item_modifier_quantity(self, order: Order, line_item_id: str, line_item_modifier_id: str,
                                           quantity: int) -> Order:
        line_item = self._find_line_item_by_id(order.line_items, line_item_id)
        line_item_modifier = (self._find_line_item_by_id(group.items, line_item_modifier_id)
                              for group in line_item.groups)

        if line_item_modifier:
            line_item_modifier.quantity = quantity

        return order

    def add_discount(self, order: Order, discount: Discount) -> Order:
        order.discounts.append(discount)

        return order

    def remove_discount(self, order: Order, discount_id: str) -> Order:
        order.discounts = [
            discount for discount in order.discounts if discount.id != discount_id
        ]

        return order

    def add_payment(self, order: Order, payment: Payment) -> Order:
        order.payments.append(payment)

        return order

    def remove_payment(self, order: Order, payment_id: str) -> Order:
        order.payments = [
            payment for payment in order.payments if payment.id != payment_id
        ]

        return order

    @staticmethod
    def _find_line_item_by_id(line_items: list[LineItem], line_item_id: str) -> LineItem:
        return find_first_by_predicate(line_items, lambda line_item: line_item.line_item_id == line_item_id)


order_service = OrderService()

__all__ = ['OrderService', 'order_service']
