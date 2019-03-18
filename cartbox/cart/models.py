
from collections import defaultdict

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from analytics import utils as analytics_utils
from analytics.stats import Stats


# varchars laaame :'(
MAX_LENGTH = 200


class CartUser(AbstractUser):

    def get_all_suggested_products(self):
        return Product.objects.all()

    def get_suggested_products(self, max=5):
        return self.get_all_suggested_products()[:max]

    def place_order(self, products):
        order = self.orders.create()
        for product in products:
            item = order.add_item(product)
        order.place()
        return order


class Category(models.Model):
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'categories'
    title = models.CharField(max_length=MAX_LENGTH)
    def __str__(self):
        return self.title


class ProductInfo(models.Model):
    """Fields shared between Product and OrderItem"""
    class Meta:
        abstract = True
        ordering = ['sku']
    title = models.CharField(max_length=MAX_LENGTH)
    sku = models.CharField(max_length=MAX_LENGTH)

class Product(ProductInfo):
    category = models.ForeignKey(Category,
        related_name='products')
    sku = models.CharField(max_length=MAX_LENGTH,
        unique=True)
    def __str__(self):
        return "({}) {}".format(self.sku, self.title)


class Order(models.Model):

    class Meta:
        ordering = ['id']

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='orders')
    placed = models.BooleanField(default=False)

    def __str__(self):
        id_msg = "(unsaved)" if self.id is None else self.id
        return "{} {}".format(self.__class__.__name__, id_msg)

    def add_item(self, product, **kwargs):
        return self.items.create(
            sku=product.sku, title=product.title,
            category=product.category,
            **kwargs)

    def items_by_category(self):
        items_by_category = defaultdict(list)
        for item in self.items.all():
            items_by_category[item.category].append(item)
        # We convert to a dict so that we can do
        # order.items_by_category.items in templates without Django
        # trying to add an 'items' key to our defaultdict... *sigh*
        return dict(items_by_category)

    def generate_items_placed_samples(self):

        # There can be multiple items generated from the same product in a
        # single order, but the analytics samples are counting the number
        # of *orders* in which a certain thing happened, not the number of
        # *times* (order items).
        # So we need to combine all items in an order which share the same
        # SKU, for the purposes of generating a single sample.
        skus = {item.sku for item in self.items.all()}
        # item_tuples: list of (sku, cat, suggested)
        item_tuples = []
        for sku in skus:
            cat = next(item.category_id
                for item in self.items.all() if item.sku == sku)
            suggested = any(item.suggested
                for item in self.items.all() if item.sku == sku)
            item_tuples.append((sku, cat, suggested))

        samples = []
        for i, (sku, cat, suggested) in enumerate(item_tuples):
            sample = analytics_utils.add_item_placed_sample(
                self.user_id, sku, cat, suggested)
            samples.append(sample)
            for sku2, cat2, suggested2 in item_tuples[i+1:]:
                sample = analytics_utils.add_items_placed_together_sample(
                    self.user_id,
                    sku, sku2, cat, cat2,
                    suggested, suggested2)
                samples.append(sample)
        return samples

    def place(self):
        """Should be called after Order has been created, and its items
        attached to it"""
        self.placed = True
        self.save()
        self.generate_items_placed_samples()


class OrderItem(ProductInfo):
    class Meta:
        ordering = ['sku']
    order = models.ForeignKey(Order,
        related_name='items')
    category = models.ForeignKey(Category)
    suggested = models.BooleanField(default=False)
    def __str__(self):
        suggested_msg = " [*]" if self.suggested else ""
        return "1 x {}{}".format(self.title, suggested_msg)


