
from .models import ItemPlacedSample, ItemsPlacedTogetherSample


def divide(x, y):
    if y == 0: return None
    return x / y


class StatsMixin:

    def get_item_placed_samples(self, user, sku, cat, suggested):
        """Returns samples for given item"""
        filter = {'user': user}
        if sku: filter['sku'] = sku
        if cat: filter['cat'] = cat
        if suggested: filter['suggested'] = suggested
        return ItemPlacedSample.objects.filter(**filter)

    def get_items_placed_together_samples_item1(
            self, user, sku, cat, suggested):
        """Returns samples where given item appears as item1"""
        filter = {'user': user}
        if sku: filter['sku1'] = sku
        if cat: filter['cat1'] = cat
        if suggested: filter['suggested1'] = suggested
        return ItemsPlacedTogetherSample.objects.filter(**filter)

    def get_items_placed_together_samples_item2(
            self, user, sku, cat, suggested):
        """Returns samples where given item appears as item2"""
        filter = {'user': user}
        if sku: filter['sku2'] = sku
        if cat: filter['cat2'] = cat
        if suggested: filter['suggested2'] = suggested
        return ItemsPlacedTogetherSample.objects.filter(**filter)

    def get_items_placed_together_samples_item1_or_item2(
            self, user, sku, cat, suggested):
        """Returns samples where given item appears as item1 or item2"""
        samples = self.get_items_placed_together_samples_item1(
            user, sku, cat, suggested)
        samples |= self.get_items_placed_together_samples_item2(
            user, sku, cat, suggested)
        return samples

    def get_items_placed_together_samples_ordered(
            self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):
        """Returns samples with given item1 and item2 (in that order)"""
        filter = {'user': user}
        if sku1: filter['sku1'] = sku1
        if sku2: filter['sku2'] = sku2
        if cat1: filter['cat1'] = cat1
        if cat2: filter['cat2'] = cat2
        if suggested1: filter['suggested1'] = suggested1
        if suggested2: filter['suggested2'] = suggested2
        return ItemsPlacedTogetherSample.objects.filter(**filter)

    def get_items_placed_together_samples(
            self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):
        """Returns samples where given item1 and item2 appear (in either
        order)"""
        samples = self.get_items_placed_together_samples_ordered(
            user, sku1, sku2, cat1, cat2, suggested1, suggested2)
        samples |= self.get_items_placed_together_samples_ordered(
            user, sku2, sku1, cat2, cat1, suggested2, suggested1)
        return samples


class Stats(StatsMixin):

    def __init__(self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):

        # 1-item samples
        self.item1_placed_samples = self.get_item_placed_samples(
            user, sku1, cat1, suggested1)
        self.item2_placed_samples = self.get_item_placed_samples(
            user, sku2, cat2, suggested2)

        # 2-item samples
        self.items_placed_together_samples = (
            self.get_items_placed_together_samples(
                user, sku1, sku2, cat1, cat2,
                suggested1, suggested2))

        # stats
        self.total1 = sum(sample.count
            for sample in self.item1_placed_samples)
        self.total2 = sum(sample.count
            for sample in self.item2_placed_samples)
        self.total_together = sum(sample.count
            for sample in self.items_placed_together_samples)
        self.together_over_total1 = divide(self.total_together, self.total1)
        self.together_over_total2 = divide(self.total_together, self.total2)
