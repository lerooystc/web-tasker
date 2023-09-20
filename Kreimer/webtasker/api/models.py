from django.db import models
from django.contrib.auth.models import User
import random
import string


class Board(models.Model):
    id_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="Host")
    members = models.ManyToManyField("auth.User", related_name="Members")
    title = models.CharField(max_length=50, default="default_for_now")
    description = models.TextField(max_length=200, default="default_for_now")
    invite_code = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Column(models.Model):
    id_board = models.ForeignKey("Board", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="default_for_now")
    number = models.IntegerField()

    def __str__(self):
        return self.title


class Task(models.Model):
    id_column = models.ForeignKey("Column", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="default_for_now")
    body = models.TextField(max_length=200, default="default_for_now")
    color = models.IntegerField()
    priority = models.IntegerField()
    finish_by = models.DateTimeField()
    taken_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
