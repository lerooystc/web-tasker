from django.urls import path
from .views import BoardView, CreateBoardView, CreateColumnView, CreateTaskView, GetBoardColumns,\
    GetUserBoards, GetColumnTasks

urlpatterns = [
    path('boards/', BoardView.as_view(), name='board-list'),
    path('create-board/', CreateBoardView.as_view(), name='create-board'),
    path('user-boards/', GetUserBoards.as_view(), name='user-boards'),
    path('create-column/', CreateColumnView.as_view(), name='create-column'),
    path('board-columns/', GetBoardColumns.as_view(), name='board-columns'),
    path('create-task/', CreateTaskView.as_view(), name='create-task'),
    path('column-tasks/', GetColumnTasks.as_view(), name='column-tasks'),
]
