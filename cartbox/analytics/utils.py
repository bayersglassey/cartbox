
from .models import SKUInOrderCounter, SKUPairInOrderCounter


def swap_keys(keys):
    """Modifies the given list of strings, changing last character from
    '1' to '2' and vice versa (if applicable).
    E.g. 'sku1' is changed to 'sku2' and vice versa."""
    def swap_key(key):
        c = key[-1:]
        if c == '1': key = "{}{}".format(key[:-1], '2')
        elif c == '2': key = "{}{}".format(key[:-1], '1')
        return key
    return [swap_key(key) for key in keys]

def swap_dict_keys(d):
    """Modifies the given dict, swapping the values of every pair of keys
    which are the same, except that one ends in '1' and the other in '2'.
    E.g. if there are keys 'sku1' and 'sku2', then their values are swapped.
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
        swap_dict_keys(d)


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

