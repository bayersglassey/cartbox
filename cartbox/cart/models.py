
from collections import defaultdict
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# varchars laaame :'(
MAX_LENGTH = 200


class CartUser(AbstractUser):
    def get_suggested_products(self, max=5):
        return Product.objects.all()[:max]


class Category(models.Model):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=MAX_LENGTH)
    def __str__(self):
        return self.title


class ProductInfo(models.Model):
    """Fields shared between Product and OrderItem"""
    class Meta:
        abstract = True
        ordering = ['sku']
    title = models.CharField(max_length=MAX_LENGTH)
    sku = models.CharField(max_length=MAX_LENGTH,
        unique=True)

class Product(ProductInfo):
    category = models.ForeignKey(Category,
        related_name='products')
    def __str__(self):
        return "({}) {}".format(self.sku, self.title)


class Order(models.Model):
    class Meta:
        ordering = ['id']
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='orders')
    def __str__(self):
        id_msg = "(unsaved)" if self.id is None else self.id
        return "{} {}".format(self.__class__.__name__, id_msg)
    def items_by_category(self):
        items_by_category = defaultdict(list)
        for item in self.items.all():
            items_by_category[item.category].append(item)
        # We convert to a dict so that we can do
        # order.items_by_category.items in templates without Django
        # trying to add an 'items' key to our defaultdict... *sigh*
        return dict(items_by_category)

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


