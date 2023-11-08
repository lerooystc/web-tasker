from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('login', LoginView.as_view(template_name='admin/login.html'))
]
