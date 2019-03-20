
from .models import SKUInOrderCounter, SKUPairInOrderCounter


def divide(x, y):
    if y == 0: return None
    return x / y


class StatsMixin:

    def get_sku_in_order_counters(self, user, sku, cat, suggested):
        """Returns counters for given SKU"""
        filter = {'user': user}
        if sku: filter['sku'] = sku
        if cat: filter['cat'] = cat
        if suggested: filter['suggested'] = suggested
        return SKUInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters_for_sku1(
            self, user, sku, cat, suggested):
        """Returns counters where given SKU appears as sku1"""
        filter = {'user': user}
        if sku: filter['sku1'] = sku
        if cat: filter['cat1'] = cat
        if suggested: filter['suggested1'] = suggested
        return SKUPairInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters_for_sku2(
            self, user, sku, cat, suggested):
        """Returns counters where given SKU appears as sku2"""
        filter = {'user': user}
        if sku: filter['sku2'] = sku
        if cat: filter['cat2'] = cat
        if suggested: filter['suggested2'] = suggested
        return SKUPairInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters_for_sku(
            self, user, sku, cat, suggested):
        """Returns counters where given SKU appears as sku1 or sku2"""
        counters = self.get_sku_pair_in_order_counters_for_sku1(
            user, sku, cat, suggested)
        counters |= self.get_sku_pair_in_order_counters_for_sku2(
            user, sku, cat, suggested)
        return counters

    def get_sku_pair_in_order_counters_ordered(
            self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):
        """Returns counters where given SKUs appear (as an
        ordered pair)"""
        filter = {'user': user}
        if sku1: filter['sku1'] = sku1
        if sku2: filter['sku2'] = sku2
        if cat1: filter['cat1'] = cat1
        if cat2: filter['cat2'] = cat2
        if suggested1: filter['suggested1'] = suggested1
        if suggested2: filter['suggested2'] = suggested2
        return SKUPairInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters(
            self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):
        """Returns counters where given SKUs appear (as an
        unordered pair"""
        counters = self.get_sku_pair_in_order_counters_ordered(
            user, sku1, sku2, cat1, cat2, suggested1, suggested2)
        counters |= self.get_sku_pair_in_order_counters_ordered(
            user, sku2, sku1, cat2, cat1, suggested2, suggested1)
        return counters


class Stats(StatsMixin):

    def __init__(self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):

        # 1-SKU counters
        self.sku1_in_order_counters = self.get_sku_in_order_counters(
            user, sku1, cat1, suggested1)
        self.sku2_in_order_counters = self.get_sku_in_order_counters(
            user, sku2, cat2, suggested2)

        # 2-SKU counters
        self.sku_pair_in_order_counters = (
            self.get_sku_pair_in_order_counters(
                user, sku1, sku2, cat1, cat2,
                suggested1, suggested2))

        # stats
        self.total1 = sum(counter.count
            for counter in self.sku1_in_order_counters)
        self.total2 = sum(counter.count
            for counter in self.sku2_in_order_counters)
        self.total_both = sum(counter.count
            for counter in self.sku_pair_in_order_counters)
        self.both_over_total1 = divide(self.total_both, self.total1)
        self.both_over_total2 = divide(self.total_both, self.total2)
