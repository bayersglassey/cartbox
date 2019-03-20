
from .models import SKUInOrderCounter, SKUPairInOrderCounter


def add_sku_in_order(user, sku, cat, suggested):
    counter, created = SKUInOrderCounter.objects.get_or_create(
        user=user, sku=sku, cat=cat, suggested=suggested)
    counter.count += 1
    counter.save()
    return counter


def add_sku_pair_in_order(user, sku1, sku2, cat1, cat2,
        suggested1, suggested2):

    if sku1 == sku2:
        raise ValueError(
            "Can't create SKUPairInOrderCounter with sku1 == sku2",
            sku1, sku2)

    kwargs = {
        'user': user,
        'sku1': sku1, 'sku2': sku2,
        'cat1': cat1, 'cat2': cat2,
        'suggested1': suggested1, 'suggested2': suggested2,
    }

    # The pair of SKUs should be unordered, so we normalize it
    # such that sku1 < sku2
    if sku1 > sku2:
        keys = [key for key in kwargs if key.endswith('1')]
        for key1 in keys:
            key2 = "{}{}".format(key1[:-1], '2')
            temp = kwargs[key1]
            kwargs[key1] = kwargs[key2]
            kwargs[key2] = temp

    counter, created = SKUPairInOrderCounter.objects.get_or_create(
        **kwargs)
    counter.count += 1
    counter.save()
    return counter

