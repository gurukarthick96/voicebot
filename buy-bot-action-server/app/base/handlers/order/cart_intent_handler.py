from app.base.handlers import OrderIntentHandlerRegistry
from app.base.intents import UserCartIntent
from app.base.resolvers import ItemResolver, item_resolver
from app.order.facades import OrderFacade


class CartIntentHandler(OrderIntentHandlerRegistry[UserCartIntent]):

    def __init__(self, item_resolver: ItemResolver):
        self.item_resolver = item_resolver

    @OrderIntentHandlerRegistry.register(UserCartIntent.ADD_ITEMS)
    def _handle_add_items(self, user_input: str, order_facade: OrderFacade):
        line_items = self.item_resolver.resolve_new_line_items_using_llm(user_input)

        order_facade.add_line_items(line_items)

    @OrderIntentHandlerRegistry.register(UserCartIntent.UPDATE_ITEMS)
    def _handle_update_items(self, user_input: str, order_facade: OrderFacade):
        line_items = self.item_resolver.resolve_existing_line_items_using_llm(user_input, order_facade.order.line_items)

        order_facade.update_line_items(line_items)

    @OrderIntentHandlerRegistry.register(UserCartIntent.DELETE_ITEMS)
    def _handle_delete_items(self, user_input: str, order_facade: OrderFacade):
        line_items = self.item_resolver.resolve_existing_line_items(user_input, order_facade.order.line_items)

        line_item_ids = [line_item.line_item_id for line_item in line_items]

        order_facade.remove_line_items(line_item_ids)


cart_intent_handler = CartIntentHandler(item_resolver)

__all__ = ['CartIntentHandler', 'cart_intent_handler']
