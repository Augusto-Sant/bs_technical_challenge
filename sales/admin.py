from django.contrib import admin
from .models import Product, Order, OrderItem

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "stock_qty", "brand")
    search_fields = ("name", "sku", "brand")
    list_filter = ("brand",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total")
    list_filter = ("created_at",)
    search_fields = ("id",)
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    list_filter = ("order", "product")
    search_fields = ("order__id", "product__name")
    ordering = ("-id",)