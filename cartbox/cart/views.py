
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
            CAT_PREFIX = 'category-'
            if not key.startswith(CAT_PREFIX): continue
            #cat_id = int(key[len(CAT_PREFIX):])
            #cat = Category.objects.get(id=cat_id)
            products = Product.objects.filter(sku__in=values)
            for product in products:
                order.items.create(
                    sku=product.sku, title=product.title,
                    category=product.category)
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

