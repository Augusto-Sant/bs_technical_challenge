from django.shortcuts import render
from sales.models import Order, OrderItem  # assuming you have these models


def order_history_view(request):
    """Display all orders with their items"""
    orders = (
        Order.objects.all().prefetch_related("items__product").order_by("-created_at")
    )

    context = {
        "orders": orders,
    }
    return render(request, "sales/order_history.html", context)
