
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

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.OrderItem
        exclude = ['id', 'order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = cart_models.Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Don't show items for orders in list view
        view = self.context.get('view')
        action = getattr(view, 'action', None)
        if action == 'list':
            self.fields.pop('items')

class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.OrderItem
        fields = ['sku']

class PlaceOrderSerializer(serializers.ModelSerializer):
    add_items = AddItemSerializer(many=True)
    class Meta:
        model = cart_models.Order
        fields = ['user', 'add_items']

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
