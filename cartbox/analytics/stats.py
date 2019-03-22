
from collections import defaultdict

from .models import SKUInOrderCounter, SKUPairInOrderCounter
from .utils import swap_keys


def divide(x, y):
    if y == 0: return None
    return x / y


class StatsMixin:

    def get_sku_in_order_counters(
            self, user=None, sku=None, cat=None, suggested=None):
        """Returns counters for given SKU"""
        filter = {}
        if user: filter['user'] = user
        if sku: filter['sku'] = sku
        if cat: filter['cat'] = cat
        if suggested: filter['suggested'] = suggested
        return SKUInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters_for_sku1(
            self, user=None, sku=None, cat=None, suggested=None):
        """Returns counters where given SKU appears as sku1"""
        filter = {}
        if user: filter['user'] = user
        if sku: filter['sku1'] = sku
        if cat: filter['cat1'] = cat
        if suggested: filter['suggested1'] = suggested
        return SKUPairInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters_for_sku2(
            self, user=None, sku=None, cat=None, suggested=None):
        """Returns counters where given SKU appears as sku2"""
        filter = {}
        if user: filter['user'] = user
        if sku: filter['sku2'] = sku
        if cat: filter['cat2'] = cat
        if suggested: filter['suggested2'] = suggested
        return SKUPairInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters_for_sku(
            self, user=None, sku=None, cat=None, suggested=None):
        """Returns counters where given SKU appears as sku1 or sku2"""
        counters = self.get_sku_pair_in_order_counters_for_sku1(
            user, sku, cat, suggested)
        counters |= self.get_sku_pair_in_order_counters_for_sku2(
            user, sku, cat, suggested)
        return counters

    def get_sku_pair_in_order_counters_ordered(
            self, user=None,
            sku1=None, sku2=None,
            cat1=None, cat2=None,
            suggested1=None, suggested2=None):
        """Returns counters where given SKUs appear (as an
        ordered pair)"""
        filter = {}
        if user: filter['user'] = user
        if sku1: filter['sku1'] = sku1
        if sku2: filter['sku2'] = sku2
        if cat1: filter['cat1'] = cat1
        if cat2: filter['cat2'] = cat2
        if suggested1: filter['suggested1'] = suggested1
        if suggested2: filter['suggested2'] = suggested2
        return SKUPairInOrderCounter.objects.filter(**filter)

    def get_sku_pair_in_order_counters(
            self, user=None,
            sku1=None, sku2=None,
            cat1=None, cat2=None,
            suggested1=None, suggested2=None,
            tag_as_swapped=False):
        """Returns counters where given SKUs appear (as an
        unordered pair)."""
        counters = self.get_sku_pair_in_order_counters_ordered(
            user, sku1, sku2, cat1, cat2, suggested1, suggested2)
        counters_swapped = self.get_sku_pair_in_order_counters_ordered(
            user, sku2, sku1, cat2, cat1, suggested2, suggested1)

        if tag_as_swapped:
            # Could we convince the database to 'tag' the second query's
            # entries for us?.. so we could then order the resulting
            # queryset and take first 10 counters or whatever, instead
            # of having to download them all and do the tagging in Python.
            for counter in counters:
                counter.swapped = False
            for counter in counters_swapped:
                counter.swapped = True
            combined_counters = set(counters) | set(counters_swapped)
            return sorted(combined_counters, reverse=True,
                key=lambda counter: counter.count)
        else:
            return (counters | counters_swapped).order_by('-count')


class Stats(StatsMixin):

    def __init__(self, user=None,
            sku1=None, sku2=None, cat1=None, cat2=None,
            suggested1=None, suggested2=None,
            suggestion_keys=None, limit=None):

        # suggestion_keys: attributes of SKUPairInOrderCounter
        # In other words, *what it is we're suggesting*.
        # Are we suggesting the best sku?.. or best (sku, cat)?..
        # Or best (sku, cat, suggested) -- e.g. we may predict that
        # user is more likely to add a given (sku, cat) *from the
        # Suggested Products widget*.
        if suggestion_keys is None:
            suggestion_keys = ['sku2']
        suggestion_keys = [key for key in suggestion_keys
            if key in ['sku2', 'cat2', 'suggested2']]
        suggestion_keys_swapped = swap_keys(suggestion_keys)


        # 1-SKU counters
        self.sku1_in_order_counters = self.get_sku_in_order_counters(
            user, sku1, cat1, suggested1)
        self.sku2_in_order_counters = self.get_sku_in_order_counters(
            user, sku2, cat2, suggested2)

        # 2-SKU counters
        self.sku_pair_in_order_counters = (
            self.get_sku_pair_in_order_counters(
                user, sku1, sku2, cat1, cat2,
                suggested1, suggested2,
                tag_as_swapped=True))

        # stats
        self.total1 = sum(counter.count
            for counter in self.sku1_in_order_counters)
        self.total2 = sum(counter.count
            for counter in self.sku2_in_order_counters)
        self.total_both = sum(counter.count
            for counter in self.sku_pair_in_order_counters)
        self.both_over_total1 = divide(self.total_both, self.total1)
        self.both_over_total2 = divide(self.total_both, self.total2)

        # self.suggestions: list of (suggestion, total2)
        # where a suggestion is a tuple of attributes of
        # SKUPairInOrderCounter
        suggestion_map = defaultdict(int)
        for counter in self.sku_pair_in_order_counters:
            # TODO: Document the meaning of this tag_as_swapped stuff.
            attrs = (suggestion_keys_swapped
                if counter.swapped else suggestion_keys)
            suggestion = tuple(
                getattr(counter, attr) for attr in attrs)
            suggestion_map[suggestion] += counter.count

        self.suggestions = sorted(suggestion_map.items(), reverse=True,
            key=lambda suggestion_and_total2: suggestion_and_total2[1])

        if limit is not None:
            self.suggestions = self.suggestions[:limit]
