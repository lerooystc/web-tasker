from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'columns', ColumnViewSet, basename='column')
router.register(r'tasks', TaskViewSet, basename='task')


urlpatterns = [
    path('', include(router.urls)),
    path('user-boards/', GetUserBoards.as_view(), name='user-boards'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', UserRegister.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
]
