
from django.db import models
from django.conf import settings


# varchars laaame :'(
MAX_LENGTH = 200


class Category(models.Model):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=MAX_LENGTH)


class ProductInfo(models.Model):
    """Fields shared between Product and OrderItem"""
    class Meta:
        abstract = True
        ordering = ['sku']
    title = models.CharField(max_length=MAX_LENGTH)
    sku = models.CharField(max_length=MAX_LENGTH)
    category = models.ForeignKey(Category)

class Product(ProductInfo):
    pass


class Order(models.Model):
    class Meta:
        ordering = ['id']
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='orders')

class OrderItem(ProductInfo):
    class Meta:
        ordering = ['sku']
    order = models.ForeignKey(Order)


