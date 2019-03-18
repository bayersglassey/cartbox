from django.test import TestCase, RequestFactory

from .models import Category, Product, Order, CartUser
from .default_data import update_or_create_cats_and_prods


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


class CartTestCase(CartTestCaseMixin, TestCase):

    def test_order_place(self):
        order = self.user.place_order([self.banana, self.apple])
