from django.contrib import admin
from .models import Board, Task, Column

admin.site.register(Task)
admin.site.register(Board)
admin.site.register(Column)
