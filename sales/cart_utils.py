"""
Cart utility functions for managing shopping carts.
"""

from sales.models import Cart


def get_or_create_cart(request):
    """
    Get or create a cart for the current session.
    Uses session to store cart_id.
    """
    cart_id = request.session.get("cart_id")

    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
            return cart
        except Cart.DoesNotExist:
            # cart was deleted, create new one
            pass

    # create new cart
    cart = Cart.objects.create()
    request.session["cart_id"] = cart.id
    return cart


def get_cart_item_count(cart):
    """
    Get total number of items in cart.
    """
    if not cart:
        return 0
    return sum(item.quantity for item in cart.items.all())
