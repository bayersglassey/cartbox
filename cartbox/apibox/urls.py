
from django.conf.urls import url, include

from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r'cart/categories', viewsets.CategoryViewSet)
router.register(r'cart/products', viewsets.ProductViewSet)
router.register(r'cart/orders', viewsets.OrderViewSet)
router.register(r'cart/orderitems', viewsets.OrderItemViewSet)
router.register(r'cart/users', viewsets.UserViewSet)
router.register(r'analytics/counters/skus_in_order',
    viewsets.SKUInOrderCounterViewSet)
router.register(r'analytics/counters/sku_pairs_in_order',
    viewsets.SKUPairInOrderCounterViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
