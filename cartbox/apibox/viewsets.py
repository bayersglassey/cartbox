
from rest_framework import views, viewsets, response
from rest_framework.decorators import action

from cart.models import Product, CartUser
from analytics.stats import Stats

from . import serializers

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = serializer_class.Meta.model.objects.all()
    search_fields = ['title']

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filter_fields = ['category']
    search_fields = ['title']

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filter_fields = ['user']

    @action(['post'], detail=False)
    def place(self, request):
        """Place a new order on POST"""

        serializer = serializers.PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Place an order for indicated user
        user = serializer.validated_data['user']
        add_items = serializer.validated_data.get('add_items', [])
        skus = [d['sku'] for d in add_items]
        products = Product.objects.filter(sku__in=skus)
        order = user.place_order(products)

        # Return serialized order data
        order_serializer = serializers.OrderSerializer(instance=order)
        return response.Response(order_serializer.data, status=201)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
    search_fields = ['username', 'email', 'first_name', 'last_name']


class SKUInOrderCounterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SKUInOrderCounterSerializer
    queryset = serializer_class.Meta.model.objects.all()

class SKUPairInOrderCounterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SKUPairInOrderCounterSerializer
    queryset = serializer_class.Meta.model.objects.all()

class StatsViewSet(viewsets.ViewSet):
    serializer_class = serializers.StatsSerializer

    # This queryset isn't really used, but it allows
    # DjangoModelPermissionsOrAnonReadOnly to look at this viewset
    # without exploding.
    # So, in order to view stats via the API, you need read permissions
    # for the user model... seems reasonable.
    queryset = CartUser.objects.all()

    def list(self, request):
        """Not really a list, but calling it so makes everything work with
        the Router"""
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        stats = Stats(**serializer.data)
        output_serializer = serializers.StatsOutputSerializer(stats)
        return response.Response(output_serializer.data)
