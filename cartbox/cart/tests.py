from django.test import TestCase, RequestFactory

from analytics.models import SKUInOrderCounter, SKUPairInOrderCounter

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

    def assertLen(self, xs, n):
        if len(xs) != n:
            raise AssertionError("len of {} != {}"
                .format(repr(xs), repr(n)))

    def assertStartsWith(self, x, y):
        if not x.startswith(y):
            raise AssertionError("{} does not start with {}"
                .format(repr(x), repr(y)))


class CartTestCase(CartTestCaseMixin, TestCase):

    def test_order_place(self):
        order = self.user.place_order([self.banana, self.apple])

        # We should get 3 counters:
        #  <SKUInOrderCounter: 1 x 4011 1549>
        #  <SKUInOrderCounter: 1 x 4101 1549>
        #  <SKUPairInOrderCounter: 1 x 4011 1549 | 4101 1549>
        counters = order._placed_counters
        self.assertEqual(len(counters), 3)

        # Check the SKUInOrderCounters
        sku_counters = [c for c in counters
            if isinstance(c, SKUInOrderCounter)]
        self.assertEqual(len(sku_counters), 2)
        banana_counters = [c for c in sku_counters
            if c.sku == self.banana.sku]
        self.assertEqual(len(banana_counters), 1)
        apple_counters = [c for c in sku_counters
            if c.sku == self.apple.sku]
        self.assertEqual(len(apple_counters), 1)

        # Check the SKUPairInOrderCounter
        sku_pair_counters = [c for c in counters
            if isinstance(c, SKUPairInOrderCounter)]
        self.assertEqual(len(sku_pair_counters), 1)
        sku_pair_counter = sku_pair_counters[0]
        # Note: SKUPairInOrderCounter guarantees sku1 < sku2.
        # banana.sku is "4011", apple.sku is "4101".
        # So sku1 should be banana, sku2 should be apple.
        self.assertEqual(sku_pair_counter.sku1, self.banana.sku)
        self.assertEqual(sku_pair_counter.sku2, self.apple.sku)

        with self.assertRaises(AssertionError):
            # Can't place an already-placed order
            order.place()

    def test_order_items_by_category(self):
        order = self.user.place_order([self.banana, self.apple, self.beef])
        items_by_category = order.items_by_category()
        self.assertEqual(set(items_by_category), {self.fruit, self.meat})

        # Check fruit items
        fruit_items = items_by_category[self.fruit]
        self.assertEqual(len(fruit_items), 2)
        self.assertEqual({i.sku for i in fruit_items},
            {self.banana.sku, self.apple.sku})

        # Check meat item
        meat_items = items_by_category[self.meat]
        self.assertEqual(len(meat_items), 1)
        self.assertEqual({i.sku for i in meat_items},
            {self.beef.sku})

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


