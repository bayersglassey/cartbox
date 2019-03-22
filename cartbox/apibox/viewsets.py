
from rest_framework import viewsets

from . import serializers

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = serializer_class.Meta.model.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = serializer_class.Meta.model.objects.all()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = serializer_class.Meta.model.objects.all()

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    queryset = serializer_class.Meta.model.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = serializer_class.Meta.model.objects.all()


class SKUInOrderCounterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SKUInOrderCounterSerializer
    queryset = serializer_class.Meta.model.objects.all()

class SKUPairInOrderCounterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SKUPairInOrderCounterSerializer
    queryset = serializer_class.Meta.model.objects.all()
