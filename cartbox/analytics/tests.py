from django.test import TestCase

from cart.tests import CartTestCaseMixin

from .views import StatsView


class AnalyticsTestCase(CartTestCaseMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.stats_view = StatsView.as_view()

    def test_basic_stats(self):
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
        self.assertEqual(context['total_together'], 1)

        request = self.factory.post('fake_url', {
            'sku1': self.apple.sku,
            'sku2': self.banana.sku,
        })
        response = self.stats_view(request)
        context = response.context_data
        self.assertEqual(context['total1'], 1)
        self.assertEqual(context['total2'], 2)
        self.assertEqual(context['total_together'], 1)
