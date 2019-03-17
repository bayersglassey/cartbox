from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^samples/search/$', login_required(views.SampleSearchView.as_view())),
]
