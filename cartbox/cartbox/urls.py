"""cartbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from cart.models import CartUser


class Home(TemplateView):
    template_name = 'index.html'

class CartUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CartUser

class RegisterView(CreateView):
    form_class = CartUserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/'
    def form_valid(self, form):
        _return = super().form_valid(form)
        login(self.request, self.object)
        return _return

urlpatterns = [
    url(r'^$', Home.as_view()),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^analytics/', include('analytics.urls', namespace='analytics')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/signup/$', RegisterView.as_view()),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
