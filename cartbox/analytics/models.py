from django.db import models

MAX_LENGTH = 200


class Counter(models.Model):
    class Meta:
        abstract = True
    count = models.IntegerField(default=0)


def get_suggested_msg(suggested):
    return ' [*]' if suggested else ''

def get_pseudo_item_msg(user, sku, cat, suggested):
    suggested_msg = get_suggested_msg(suggested)
    return "{} {}{}".format(sku, cat, suggested_msg)

def get_item_msg(user, sku, cat, suggested, product=None, category=None):
    from cart.models import Product, Category
    if product is None:
        product = Product.objects.filter(sku=sku).first()
    if category is None:
        category = Category.objects.filter(id=cat).first()
    title = "<NOT FOUND>" if product is None else product.title
    cat_title = "<NOT FOUND>" if category is None else category.title
    suggested_msg = get_suggested_msg(suggested)
    return "({}) {} ({}){}".format(sku, title, cat_title, suggested_msg)


class SKUInOrderCounter(Counter):
    user = models.CharField(max_length=MAX_LENGTH)
    sku = models.CharField(max_length=MAX_LENGTH)
    cat = models.CharField(max_length=MAX_LENGTH)
    suggested = models.BooleanField(default=False)
    def __str__(self):
        return self.get_str()
    def fancy_str(self):
        """For use in templates"""
        return self.get_str(fancy=True)
    def get_str(self, fancy=False):
        if fancy:
            item_msg = get_item_msg(
                self.user, self.sku, self.cat, self.suggested)
        else:
            item_msg = get_pseudo_item_msg(
                self.user, self.sku, self.cat, self.suggested)
        return "{} x {}".format(self.count, item_msg)


class SKUPairInOrderCounter(Counter):
    user = models.CharField(max_length=MAX_LENGTH)

    # NOTE: it should always be the case that sku1 < sku2.
    # That's because we're counting unordered pairs of SKUs.
    # Also, sku == sku makes no sense and indicates somebody having
    # made an error somewhere.
    sku1 = models.CharField(max_length=MAX_LENGTH)
    sku2 = models.CharField(max_length=MAX_LENGTH)

    cat1 = models.CharField(max_length=MAX_LENGTH)
    cat2 = models.CharField(max_length=MAX_LENGTH)
    suggested1 = models.BooleanField(default=False)
    suggested2 = models.BooleanField(default=False)

    def __str__(self):
        return self.get_str()
    def fancy_str(self):
        return self.get_str(fancy=True)
    def get_str(self, fancy=False):
        if fancy:
            item1_msg = get_item_msg(
                self.user, self.sku1, self.cat1, self.suggested1)
            item2_msg = get_item_msg(
                self.user, self.sku2, self.cat2, self.suggested2)
        else:
            item1_msg = get_pseudo_item_msg(
                self.user, self.sku1, self.cat1, self.suggested1)
            item2_msg = get_pseudo_item_msg(
                self.user, self.sku2, self.cat2, self.suggested2)
        return "{} x {} | {}".format(self.count, item1_msg, item2_msg)

