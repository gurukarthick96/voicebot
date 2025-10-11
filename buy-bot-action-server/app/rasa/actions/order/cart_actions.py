from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from app.base.handlers.order import cart_intent_handler
from app.base.intents import UserCartIntent
from app.order.models import Order
from app.utils import to_enum, generate_cart_summary


class ActionParseUserInputAndIntentForCartFromLLM(Action):
    def name(self) -> Text:
        return 'action_parse_user_intent_for_cart_from_llm'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input_text = tracker.latest_message.get('text')
        user_intent_for_cart_slot_text = tracker.get_slot('user_intent_for_cart')

        user_input = user_input_text

        user_cart_intent = to_enum(UserCartIntent, user_intent_for_cart_slot_text).value

        return [
            SlotSet('user_intent_for_cart', None),

            SlotSet('parsed_user_input', user_input),
            SlotSet('parsed_user_intent', user_cart_intent),
        ]


class ActionHandleUserIntentForCart(Action):
    def name(self) -> Text:
        return 'action_handle_user_intent_for_cart'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        parsed_user_input_slot_text = tracker.get_slot('parsed_user_input')
        parsed_user_intent_slot_text = tracker.get_slot('parsed_user_intent')
        order_slot_dict = tracker.get_slot('order')

        user_input = parsed_user_input_slot_text

        user_cart_intent = to_enum(UserCartIntent, parsed_user_intent_slot_text)

        order = cart_intent_handler.handle(user_cart_intent, user_input, order_slot_dict)

        item_count = len(order.line_items)

        return [
            SlotSet('parsed_user_input', None),
            SlotSet('parsed_user_intent', None),

            SlotSet('cart_item_count', item_count),
            SlotSet('order', order),
        ]


class ActionCheckoutCart(Action):
    def name(self) -> Text:
        return 'action_checkout_cart'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_slot_dict = tracker.get_slot('order')

        order = Order.from_dict(order_slot_dict)

        cart_summary = generate_cart_summary(order)

        return [
            SlotSet('parsed_user_input', None),
            SlotSet('parsed_user_intent', None),

            SlotSet('cart_summary', cart_summary),
        ]
