from django.test import TestCase, RequestFactory

from .models import Category, Product, Order, CartUser
from .default_data import (
    update_or_create_cats_and_prods, updated_or_created)
from . import views


class CartRequestFactory(RequestFactory):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def request(self, *args, **kwargs):
        request = super().request(*args, **kwargs)
        request.user = self.user
        return request


class CartTestCaseMixin:

    def setUp(self):
        self.user = CartUser.objects.create()

        self.factory = CartRequestFactory(self.user)

        update_or_create_cats_and_prods(verbose=False)
        self.fruit = Category.objects.get(title="Fruit")
        self.veg = Category.objects.get(title="Veg")
        self.meat = Category.objects.get(title="Meat")
        self.banana = Product.objects.get(sku='4011')
        self.apple = Product.objects.get(sku='4101')
        self.beef = Product.objects.get(sku='210001')
        self.veal = Product.objects.get(sku='210007')

    def assertStartsWith(self, x, y):
        if not x.startswith(y):
            raise AssertionError("{} does not start with {}"
                .format(repr(x), repr(y)))


class CartTestCase(CartTestCaseMixin, TestCase):

    def test_order_place(self):
        order = self.user.place_order([self.banana, self.apple])

    def test_order_items_by_category(self):
        order = self.user.place_order([self.banana, self.apple])
        items_by_category = order.items_by_category()

    def test_misc(self):
        # Category.__str__
        str(self.meat)

        # Product.__str__
        str(self.apple)

        # Order.__str__
        order = self.user.place_order([self.banana, self.apple])
        str(order)

        # OrderItem.__str__
        str(order.items.first())

        # updated_or_created
        updated_or_created(True, order)


class CartViewsTestCase(CartTestCaseMixin, TestCase):

    def setUp(self):
        super().setUp()

        self.shop_view = views.ShopView.as_view()
        self.order_view = views.OrderView.as_view()
        self.orders_view = views.OrdersView.as_view()
        self.clear_account_view = views.ClearAccountView.as_view()

    def test_shop_view(self):
        request = self.factory.get('fake_url')
        response = self.shop_view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('fake_url', {
            'sku': self.banana.sku,
            'sku': self.apple.sku,
            'suggested-sku': self.beef.sku,
        })
        response = self.shop_view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('fake_url', {
            'sku': self.banana.sku,
            'sku': self.apple.sku,
            'suggested-sku': self.beef.sku,
            'place-order': '',
        })
        response = self.shop_view(request)
        self.assertStartsWith(response['Location'], '/cart/order/')

    def test_order_view(self):
        order = self.user.place_order([self.banana, self.apple])
        request = self.factory.get('fake_url')
        response = self.order_view(request, pk=order.id)
        self.assertEqual(response.status_code, 200)

    def test_orders_view(self):
        request = self.factory.get('fake_url')
        response = self.orders_view(request)
        self.assertEqual(response.status_code, 200)

    def test_clear_account_view(self):
        request = self.factory.post('fake_url', {})
        response = self.clear_account_view(request)
        self.assertEqual(response['Location'], '/')


