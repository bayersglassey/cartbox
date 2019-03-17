
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from .models import Category, Product, Order


class ShopView(CreateView):
    model = Order
    fields = []
    template_name = 'cart/shop.html'
    success_url = '/cart/order/{id}/'
    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context
    def form_valid(self, form):
        request = self.request
        user = request.user
        order = user.orders.create()
        for key, values in request.POST.lists():
            if key not in ['sku', 'suggested-sku']: continue
            suggested = key == 'suggested-sku'
            products = Product.objects.filter(sku__in=values)
            for product in products:
                order.items.create(
                    sku=product.sku, title=product.title,
                    category=product.category,
                    suggested=suggested)
        order.place()
        self.object = order
        return FormMixin.form_valid(self, form)

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

