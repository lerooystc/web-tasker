from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
]
