"""
Context processors for sales app.
"""

from sales.cart_utils import get_or_create_cart, get_cart_item_count


def cart_context(request):
    """
    Add cart information to template context.
    """
    cart = get_or_create_cart(request)
    cart_item_count = get_cart_item_count(cart)

    return {
        "cart": cart,
        "cart_item_count": cart_item_count,
    }
