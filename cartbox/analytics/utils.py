
from .models import SKUInOrderCounter, SKUPairInOrderCounter


def swap_keys_1_2(d):
    """Modifies the given dict, swapping the values of every pair of keys
    which are the same, except that one ends in '1' and the other in '2'.
    E.g. if there are keys 'abc1' and 'abc2', then their values are swapped.
    """
    for key1 in d:
        if not key1.endswith('1'): continue
        key2 = "{}{}".format(key1[:-1], '2')
        if key2 not in d: continue
        temp = d[key1]
        d[key1] = d[key2]
        d[key2] = temp


def normalize_sku_pair_keys(d):
    """The pairs of SKUs used with SKUPairInOrderCounter should be
    unordered, so we normalize the arguments to functions which
    deal with them, such that sku1 < sku2."""
    sku1 = d.get('sku1')
    sku2 = d.get('sku2')
    if sku1 is None: return
    if sku2 is None: return
    if sku1 > sku2:
        swap_keys_1_2(d)


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

    normalize_sku_pair_keys(kwargs)

    counter, created = SKUPairInOrderCounter.objects.get_or_create(
        **kwargs)
    counter.count += 1
    counter.save()
    return counter

