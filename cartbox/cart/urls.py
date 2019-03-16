from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^shop/$', login_required(views.ShopView.as_view()), name='shop'),
    url(r'^order/(?P<pk>\d+)/$', login_required(views.OrderView.as_view()), name='order'),
    url(r'^orders/$', login_required(views.OrdersView.as_view()), name='orders'),
]
