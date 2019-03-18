
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django import forms

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
                item = order.add_item(product, suggested=suggested)
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



class ClearAccountView(FormView):
    template_name = 'cart/clear_account.html'
    form_class = forms.Form
    success_url = '/'
    def form_valid(self, form):
        from analytics.models import ItemPlacedSample
        from analytics.models import ItemsPlacedTogetherSample

        request = self.request
        user = request.user
        print("Clearing account for user: {}".format(user))
        print("Deleted: {}".format(user.orders.all().delete()))
        print("Deleted: {}".format(
            ItemPlacedSample.objects.filter(user=user.id).delete()))
        print("Deleted: {}".format(
            ItemsPlacedTogetherSample.objects.filter(user=user.id).delete()))
        print("OK!")
        return super().form_valid(form)
