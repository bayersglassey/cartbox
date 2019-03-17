
from .models import ItemPlacedSample, ItemsPlacedTogetherSample


def add_item_placed_sample(user, item):
    sample, created = ItemPlacedSample.objects.get_or_create(
        user=user, sku=item.sku, cat=item.category_id,
        suggested=item.suggested)
    sample.count += 1
    sample.save()
    return sample



def items_sorted(item1, item2):
    if item1.sku < item2.sku:
        item_temp = item2
        item2 = item1
        item1 = item_temp
    return item1, item2

def add_items_placed_together_sample(user, item1, item2):
    # The same pair of items should be added to the same sample no matter
    # which order they are given in
    item1, item2 = items_sorted(item1, item2)

    sample, created = ItemsPlacedTogetherSample.objects.get_or_create(
        user=user,
        sku1=item1.sku, sku2=item2.sku,
        cat1=item1.category_id, cat2=item2.category_id,
        suggested1=item1.suggested, suggested2=item1.suggested)
    sample.count += 1
    sample.save()
    return sample

