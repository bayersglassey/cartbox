
from rest_framework import serializers

from cart import models as cart_models
from analytics import models as analytics_models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.Order
        fields = ['user', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.OrderItem
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.CartUser
        fields = '__all__'


class SKUInOrderCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = analytics_models.SKUInOrderCounter
        fields = '__all__'

class SKUPairInOrderCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = analytics_models.SKUPairInOrderCounter
        fields = '__all__'
