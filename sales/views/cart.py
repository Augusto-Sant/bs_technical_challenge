"""
Cart views for managing shopping cart operations.
"""

from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from sales.models import Product, CartItem
from sales.cart_utils import get_or_create_cart, get_cart_item_count


@require_http_methods(["POST"])
def add_to_cart_view(request, product_id):
    """
    Add a product to the cart or increment quantity if already in cart.
    Returns HTMX response with updated cart button and navbar count.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)

    # check stock availability
    if product.stock_qty == 0:
        return TemplateResponse(
            request,
            "sales/_cart_button_add.html",
            {
                "product": product,
                "cart_item": None,
                "error": "Product is out of stock",
                "cart_item_count": get_cart_item_count(cart),
            },
            status=400,
        )

    # get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": 1}
    )

    if not created:
        # increment quantity if already in cart but respect stock limit
        if cart_item.quantity < product.stock_qty:
            cart_item.quantity += 1
            cart_item.save()
        else:
            # already at max stock
            pass

    # get updated cart item
    cart_item.refresh_from_db()

    context = {
        "product": product,
        "cart_item": cart_item,
        "cart_item_count": get_cart_item_count(cart),
    }

    return TemplateResponse(
        request,
        "sales/_cart_button_quantity.html",
        context,
    )


def update_cart_quantity_view(request, product_id):
    """
    Update quantity of a product in the cart.
    Handles increment, decrement, and removal (quantity 0).
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        # Item not in cart, return add button
        return TemplateResponse(
            request,
            "sales/_cart_button_add.html",
            {
                "product": product,
                "cart_item": None,
                "cart_item_count": get_cart_item_count(cart),
            },
        )

    # get action (increment, decrement, or set)
    action = request.GET.get("action", "set")

    if action == "increment":
        quantity = cart_item.quantity + 1
    elif action == "decrement":
        quantity = cart_item.quantity - 1
    else:
        # set from input field
        try:
            quantity = int(request.GET.get("quantity", cart_item.quantity))
        except (ValueError, TypeError):
            quantity = cart_item.quantity

    # validate quantity
    if quantity <= 0:
        # remove from cart
        cart_item.delete()
        return TemplateResponse(
            request,
            "sales/_cart_button_add.html",
            {
                "product": product,
                "cart_item": None,
                "cart_item_count": get_cart_item_count(cart),
            },
        )

    # enforce stock limit
    if quantity > product.stock_qty:
        quantity = product.stock_qty

    # update quantity
    cart_item.quantity = quantity
    cart_item.save()

    context = {
        "product": product,
        "cart_item": cart_item,
        "cart_item_count": get_cart_item_count(cart),
    }

    return TemplateResponse(
        request,
        "sales/_cart_button_quantity.html",
        context,
    )
