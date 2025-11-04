from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from sales.models import CartItem, Order, OrderItem  # assuming you have these models
from sales.cart_utils import get_or_create_cart
from django.template.response import TemplateResponse


def review_view(request):
    """Display cart items and total before placing the order."""
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart).select_related("product")

    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total": total,
    }
    return TemplateResponse(request, "sales/review.html", context)


@require_http_methods(["POST"])
def place_order_view(request):
    """Create order, clear cart, and redirect to home."""
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart).select_related("product")

    if not cart_items.exists():
        return redirect("sales:products")

    order = Order.objects.create(
        total=sum(item.product.price * item.quantity for item in cart_items),
    )

    # create orderitems
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
        # reduce stock
        item.product.stock_qty -= item.quantity
        item.product.save()

    # clear cart
    cart_items.delete()

    return redirect("sales:home")
