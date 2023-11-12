from django.urls import path
from .views import *

urlpatterns = [
    path('boards/', GetBoards.as_view(), name='board-list'),
    path('get-board/<int:pk>', GetBoard.as_view(), name='get-board'),
    path('create-board/', CreateBoardView.as_view(), name='create-board'),
    path('user-boards/', GetUserBoards.as_view(), name='user-boards'),
    path('create-column/', CreateColumnView.as_view(), name='create-column'),
    path('board-columns/<int:pk>', GetBoardColumns.as_view(), name='board-columns'),
    path('create-task/', CreateTaskView.as_view(), name='create-task'),
    path('column-tasks/<int:pk>', GetColumnTasks.as_view(), name='column-tasks'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', UserRegister.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
]
