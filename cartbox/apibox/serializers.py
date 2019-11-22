
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
        exclude = ['id']

class SKUPairInOrderCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = analytics_models.SKUPairInOrderCounter
        exclude = ['id']

class StatsSerializer(serializers.Serializer):
    """Serializer for the kwargs of the Stats class constructor"""
    user = serializers.PrimaryKeyRelatedField(required=False,
        queryset=cart_models.CartUser.objects.all())
    sku1 = serializers.CharField(required=False)
    sku2 = serializers.CharField(required=False)
    cat1 = serializers.CharField(required=False)
    cat2 = serializers.CharField(required=False)
    suggested1 = serializers.BooleanField(required=False)
    suggested2 = serializers.BooleanField(required=False)
    limit = serializers.IntegerField(required=False)

class StatsOutputSerializer(serializers.Serializer):
    """Serializer for the attributes of the Stats class"""
    total1 = serializers.IntegerField()
    total2 = serializers.IntegerField()
    total_both = serializers.IntegerField()
    both_over_total1 = serializers.FloatField()
    both_over_total2 = serializers.FloatField()
    sku1_in_order_counters = SKUInOrderCounterSerializer(many=True)
    sku2_in_order_counters = SKUInOrderCounterSerializer(many=True)
    sku_pair_in_order_counters = SKUPairInOrderCounterSerializer(many=True)
    suggestions = serializers.ListField()

    def __init__(self, stats):
        # Yes, __dict__ is fairly ganky, but it seems to make sense in
        # this case, since the serializer is specifying the fields.
        data = stats.__dict__.copy()

        # stats.suggestions terrifies me, I do not remember why it has
        # such a weird format.
        # We transform it into something nicer before showing it to
        # the user.
        data["suggestions"] = [
            {"sku": sku, "count": count}
            for ((sku,), count) in stats.suggestions]

        super().__init__(data)
