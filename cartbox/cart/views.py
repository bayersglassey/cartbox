
from django.views.generic import ListView, DetailView, CreateView

from .models import Category, Product, Order


class ShopView(CreateView):
    model = Order
    fields = []
    template_name = 'cart/shop.html'
    success_url = 'cart/orders/{id}/'

class UserOrdersViewMixin:
    model = Order
    def get_queryset(self):
        request = self.request
        user = request.user
        return user.orders.all()

class OrdersView(UserOrdersViewMixin, ListView):
    template_name = 'cart/orders.html'

class OrderView(UserOrdersViewMixin, DetailView):
    template_name = 'cart/order.html'

