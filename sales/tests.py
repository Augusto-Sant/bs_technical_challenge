from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from sales.models import Product, CartItem, Order, OrderItem
from sales.views import (
    products_view,
    product_detail_modal_view,
    add_to_cart_view,
    update_cart_quantity_view,
    order_history_view,
)
from django.utils import timezone


def add_session_to_request(request):
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()


class ProductViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = Product.objects.create(
            name="Laptop",
            sku="LAP123",
            price=499.99,
            stock_qty=10,
        )

    def _get_request(self, url, **kwargs):
        """Helper to get a request with session enabled."""
        request = self.factory.get(url, **kwargs)
        add_session_to_request(request)
        return request

    def test_products_view_returns_products(self):
        url = reverse("sales:products")
        request = self._get_request(url)
        response = products_view(request)
        response.render()
        products = response.context_data["products"]
        self.assertIn(self.product, products)
        self.assertEqual(response.status_code, 200)

    def test_products_view_filters_query(self):
        Product.objects.create(name="Phone", sku="PH123", price=199.99, stock_qty=5)
        url = reverse("sales:products") + "?q=Laptop"
        request = self._get_request(url)
        response = products_view(request)
        response.render()
        products = response.context_data["products"]
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Laptop")

    def test_product_detail_modal_view_returns_product(self):
        url = reverse("sales:product_detail_modal", args=[self.product.id])
        request = self._get_request(url)
        response = product_detail_modal_view(request, product_id=self.product.id)
        response.render()
        product = response.context_data["product"]
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(response.status_code, 200)


class CartViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = Product.objects.create(
            name="Headphones",
            sku="HD123",
            price=99.99,
            stock_qty=3,
        )

    def _post_request(self, url, **kwargs):
        request = self.factory.post(url, **kwargs)
        add_session_to_request(request)
        # keep the same session across calls
        if hasattr(self, "session"):
            request.session = self.session
        else:
            self.session = request.session
        return request

    def _get_request(self, url, **kwargs):
        request = self.factory.get(url, **kwargs)
        add_session_to_request(request)
        if hasattr(self, "session"):
            request.session = self.session
        else:
            self.session = request.session
        return request

    def test_add_to_cart_creates_cart_item(self):
        url = reverse("sales:add_to_cart", args=[self.product.id])
        request = self._post_request(url)
        response = add_to_cart_view(request, product_id=self.product.id)
        response.render()
        cart_item = CartItem.objects.first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 1)
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_increments_existing_item(self):
        url = reverse("sales:add_to_cart", args=[self.product.id])
        request = self._post_request(url)
        add_to_cart_view(request, product_id=self.product.id)
        # add again
        request2 = self._post_request(url)
        add_to_cart_view(request2, product_id=self.product.id)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart_respects_stock_limit(self):
        url = reverse("sales:add_to_cart", args=[self.product.id])
        for _ in range(5):
            request = self._post_request(url)
            add_to_cart_view(request, product_id=self.product.id)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, self.product.stock_qty)  # capped

    def test_update_cart_increment_increases_quantity(self):
        url = reverse("sales:add_to_cart", args=[self.product.id])
        # first add item
        request = self._post_request(url)
        add_to_cart_view(request, product_id=self.product.id)

        # now increment
        request2 = self._get_request(
            reverse("sales:update_cart_quantity", args=[self.product.id]),
            data={"action": "increment"},
        )
        update_cart_quantity_view(request2, product_id=self.product.id)

        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 2)

    def test_update_cart_decrement_removes_item(self):
        url = reverse("sales:add_to_cart", args=[self.product.id])
        request = self._post_request(url)
        add_to_cart_view(request, product_id=self.product.id)

        request2 = self._get_request(
            reverse("sales:update_cart_quantity", args=[self.product.id]),
            data={"action": "decrement"},
        )
        update_cart_quantity_view(request2, product_id=self.product.id)

        self.assertEqual(CartItem.objects.count(), 0)


class OrderHistoryViewTests(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name="Laptop", sku="LP001", price=1200, stock_qty=5
        )
        self.product2 = Product.objects.create(
            name="Mouse", sku="MS001", price=50, stock_qty=10
        )

        self.order1 = Order.objects.create(created_at=timezone.now(), total=1200)
        self.order2 = Order.objects.create(created_at=timezone.now(), total=100)

        OrderItem.objects.create(
            order=self.order1,
            product=self.product1,
            quantity=1,
            price=self.product1.price,
        )
        OrderItem.objects.create(
            order=self.order2,
            product=self.product2,
            quantity=2,
            price=self.product2.price,
        )

    def test_order_history_renders_orders(self):
        url = reverse("sales:order_history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("orders", response.context)
        orders = list(response.context["orders"])
        self.assertEqual(orders, [self.order2, self.order1])
