from app.order.models import Order


def generate_cart_summary(order: Order) -> str:
    if not order.line_items:
        return 'Your cart is currently empty.'

    parts = [f'{item.quantity} {item.name}' for item in order.line_items]

    if len(parts) == 1:
        details = parts[0]
    elif len(parts) == 2:
        details = ' and '.join(parts)
    else:
        details = ', '.join(parts[:-1]) + f', and {parts[-1]}'

    return f'Your cart summary includes {details}. The total amount is ${order.total_amount:.2f}.'
