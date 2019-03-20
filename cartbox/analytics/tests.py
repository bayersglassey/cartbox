from django.test import TestCase

from cart.tests import CartTestCaseMixin

from . import views, utils
from .stats import Stats


class AnalyticsTestCase(CartTestCaseMixin, TestCase):

    def test_basic_stats(self):
        order1 = self.user.place_order([self.banana, self.apple])
        order2 = self.user.place_order([self.banana])

        stats = Stats(self.user.id,
            self.banana.sku, self.apple.sku,
            self.fruit.id, self.fruit.id,
            False, False)
        self.assertEqual(stats.total1, 2)
        self.assertEqual(stats.total2, 1)
        self.assertEqual(stats.total_both, 1)

        stats = Stats(self.user.id,
            self.apple.sku, self.banana.sku,
            self.fruit.id, self.fruit.id,
            False, False)
        self.assertEqual(stats.total1, 1)
        self.assertEqual(stats.total2, 2)
        self.assertEqual(stats.total_both, 1)

        # SKUInOrderCounter.__str__
        counter = stats.sku1_in_order_counters[0]
        str(counter)

        # SKUPairInOrderCounter.__str__
        counter = stats.sku_pair_in_order_counters[0]
        str(counter)

    def test_cant_count_sku_with_itself(self):
        with self.assertRaises(ValueError):
            utils.add_sku_pair_in_order(self.user.id,
                self.banana.sku, self.banana.sku,
                self.fruit.id, self.fruit.id,
                False, False)


class AnalyticsViewsTestCase(CartTestCaseMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.stats_view = views.StatsView.as_view()
        self.counter_view = views.CounterView.as_view()

    def test_stats_view(self):
        order1 = self.user.place_order([self.banana, self.apple])
        order2 = self.user.place_order([self.banana])

        request = self.factory.post('fake_url', {
            'sku1': self.banana.sku,
            'sku2': self.apple.sku,
        })
        response = self.stats_view(request)
        context = response.context_data
        self.assertEqual(context['total1'], 2)
        self.assertEqual(context['total2'], 1)
        self.assertEqual(context['total_both'], 1)

        request = self.factory.post('fake_url', {
            'sku1': self.apple.sku,
            'sku2': self.banana.sku,
        })
        response = self.stats_view(request)
        context = response.context_data
        self.assertEqual(context['total1'], 1)
        self.assertEqual(context['total2'], 2)
        self.assertEqual(context['total_both'], 1)

        # SKUInOrderCounter.fancy_str
        # SKUPairInOrderCounter.fancy_str
        response.render()

    def test_counter_view(self):
        order1 = self.user.place_order([self.banana, self.apple])
        order2 = self.user.place_order([self.banana])

        request = self.factory.post('fake_url', {
            'sku': self.banana.sku,
        })
        response = self.counter_view(request)
        self.assertEqual(response.status_code, 200)
        context = response.context_data
        counters = context['sku_in_order_counters']
        self.assertLen(counters, 1)
        counter = counters[0]
        self.assertEqual(counter.count, 2)

