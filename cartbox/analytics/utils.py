
from .models import ItemPlacedSample, ItemsPlacedTogetherSample


def add_item_placed_sample(user, sku, cat, suggested):
    sample, created = ItemPlacedSample.objects.get_or_create(
        user=user, sku=sku, cat=cat, suggested=suggested)
    sample.count += 1
    sample.save()
    return sample


def add_items_placed_together_sample(user, sku1, sku2, cat1, cat2,
        suggested1, suggested2):

    if sku1 == sku2:
        raise ValueError(
            "Can't create ItemsPlacedTogetherSample with sku1 == sku2",
            sku1, sku2)

    kwargs = {
        'user': user,
        'sku1': sku1, 'sku2': sku2,
        'cat1': cat1, 'cat2': cat2,
        'suggested1': suggested1, 'suggested2': suggested2,
    }

    # The same pair of items should be added to the same sample no matter
    # which order they are given in
    # (So we force them to come in order of sku1 < sku2)
    if sku1 > sku2:
        keys = [key for key in kwargs if key.endswith('1')]
        for key1 in keys:
            key2 = "{}{}".format(key1[:-1], '2')
            temp = kwargs[key1]
            kwargs[key1] = kwargs[key2]
            kwargs[key2] = temp

    sample, created = ItemsPlacedTogetherSample.objects.get_or_create(
        **kwargs)
    sample.count += 1
    sample.save()
    return sample

