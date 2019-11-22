
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django import forms

from .models import Category, Product, Order

from analytics.stats import Stats


class ShopView(CreateView):
    """The main e-commerce view.
    Shows user all the products, organized by category in a multi-select
    widget.
    There are 2 submit buttons, each resulting in a different behaviour
    on POST:
        * Update Cart: reloads the page showing user suggested products
            based on the ones they had selected
        * Place Order: places an order using products user selected, and
            redirects to order's page
    """

    model = Order
    fields = []
    template_name = 'cart/shop.html'
    success_url = '/cart/order/{id}/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['suggested_products'] = self.get_suggested_products()
        return context

    def get_suggested_product(self, user, cart_products, product):
        """Using analytics for given user and their selected products,
        returns a suggested product or None."""
        # TODO: Make this less crappy.
        # Although really, this method shouldn't exist at all...
        # get_suggested_products should combine the suggestions for
        # all cart products somehow, and take the first N of those,
        # or whatever.
        stats = Stats(user.id, sku1=product.sku)
        suggested_skus = [sku for ((sku,), count) in stats.suggestions]
        if suggested_skus:
            sku = suggested_skus[0]
            return Product.objects.get(sku=sku)
        return None

    def get_suggested_products(self):
        """Using analytics for user and their selected products, returns
        a list of suggested products"""
        request = self.request
        user = request.user
        cart_products = self.get_cart_products()
        suggested_products = []
        for product in cart_products:
            suggested_product = self.get_suggested_product(
                user, cart_products, product)
            if suggested_product is None: continue
            suggested_products.append(suggested_product)
        return suggested_products

    def get_cart_products(self):
        """Returns list of products, based on the skus in request.POST"""
        request = self.request
        user = request.user

        # There are 2 multi-select widgets, one showing all skus organized
        # by category, the other showing suggested skus
        skus = request.POST.getlist('sku')
        suggested_skus = request.POST.getlist('suggested-sku')

        # Get products & suggested products from database
        products = list(Product.objects.filter(sku__in=skus))
        suggested_products = list(Product.objects.filter(
            sku__in=suggested_skus))

        # Poke a secret attribute onto suggested products so we can tell
        # them apart
        for product in suggested_products:
            product._suggested = True

        # Return all products as a single list
        return products + suggested_products

    def form_valid(self, form):
        request = self.request
        user = request.user

        if 'place-order' in request.POST:
            # User clicked "Place Order".
            # Place an order & redirect to its page.
            order = user.orders.create()
            products = self.get_cart_products()
            for product in products:
                # Check for secret attribute poked on by get_cart_products
                suggested = getattr(product, '_suggested', False)
                item = order.add_item(product, suggested=suggested)
            order.place()
            self.object = order
            return FormMixin.form_valid(self, form)

        # User clicked "Update Cart".
        # Just re-render the page, get_context_data() and friends will
        # peek at request.POST and send the template a list of suggested
        # products to render
        return self.form_invalid(form)

class UserOrdersViewMixin:
    """Show all orders for request.user"""
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
    """Deletes request.user's orders and analytics counters on POST"""
    template_name = 'cart/clear_account.html'
    form_class = forms.Form
    success_url = '/'
    def form_valid(self, form):
        from analytics.models import SKUInOrderCounter
        from analytics.models import SKUPairInOrderCounter

        request = self.request
        user = request.user
        print("Clearing account for user: {}".format(user))
        print("Deleted: {}".format(user.orders.all().delete()))
        print("Deleted: {}".format(
            SKUInOrderCounter.objects.filter(user=user.id).delete()))
        print("Deleted: {}".format(
            SKUPairInOrderCounter.objects.filter(user=user.id).delete()))
        print("OK!")
        return super().form_valid(form)
