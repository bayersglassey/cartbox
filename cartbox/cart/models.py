
from django.db import models
from django.conf import settings


# varchars laaame :'(
MAX_LENGTH = 200


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

class OrderItem(ProductInfo):
    class Meta:
        ordering = ['sku']
    order = models.ForeignKey(Order,
        related_name='items')
    category = models.ForeignKey(Category)
    def __str__(self):
        return "1 x {}".format(self.title)


