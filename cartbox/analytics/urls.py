from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^counters/$', login_required(views.CounterView.as_view())),
    url(r'^stats/$', login_required(views.StatsView.as_view())),
]
