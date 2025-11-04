from django.urls import path
import sales.views as views

app_name = "sales"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("products/", views.products_view, name="products"),
    path(
        "products/<int:product_id>/modal/",
        views.product_detail_modal_view,
        name="product_detail_modal",
    ),
    path("cart/add/<int:product_id>/", views.add_to_cart_view, name="add_to_cart"),
    path(
        "cart/update/<int:product_id>/",
        views.update_cart_quantity_view,
        name="update_cart_quantity",
    ),
]
