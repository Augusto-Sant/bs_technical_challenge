from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from sales.models import Product, CartItem
from sales.cart_utils import get_or_create_cart

__all__ = ["products_view", "product_detail_modal_view"]


def products_view(request):
    """
    Display all products with optional search filtering.
    Supports both full page load and HTMX partial updates.
    """
    query = request.GET.get("q", "").strip()
    cart = get_or_create_cart(request)

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    products = products.order_by("name")

    # get cart items for products to show correct button state
    cart_items = {
        item.product_id: item
        for item in CartItem.objects.filter(cart=cart, product__in=products)
    }

    context = {
        "products": products,
        "query": query,
        "cart_items": cart_items,
    }

    if request.headers.get("HX-Request"):
        return TemplateResponse(
            request,
            "sales/_product_list.html",
            context,
        )
    return TemplateResponse(
        request,
        "sales/products.html",
        context,
    )


def product_detail_modal_view(request, product_id):
    """
    Return the product detail modal content for HTMX.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)

    # check if product is in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        cart_item = None

    context = {
        "product": product,
        "cart_item": cart_item,
    }

    return TemplateResponse(
        request,
        "sales/_product_detail_modal.html",
        context,
    )
