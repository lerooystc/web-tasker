from django.db import models
import random
import string


def generate_unique_code():
    length = 8

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Board.objects.filter(invite_code=code).count() == 0:
            break

    return code


class Board(models.Model):
    id_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user_boards")
    members = models.ManyToManyField("auth.User", related_name="member_boards")
    title = models.CharField(max_length=50, default="default_for_now")
    description = models.TextField(max_length=200, default="default_for_now")
    invite_code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Column(models.Model):
    id_board = models.ForeignKey("Board", related_name='columns', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="default_for_now")
    number = models.IntegerField()

    def __str__(self):
        return self.title


class Task(models.Model):
    id_column = models.ForeignKey("Column", related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="default_for_now")
    body = models.TextField(max_length=200, default="default_for_now")
    order = models.IntegerField(default=0)
    color = models.IntegerField()
    priority = models.IntegerField()
    finish_by = models.DateTimeField()
    taken_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class Note(models.Model):
    id_board = models.ForeignKey("Board", related_name='notes', on_delete=models.CASCADE, blank=True, null=True)
    id_task = models.ForeignKey("Task", related_name='notes', on_delete=models.CASCADE, blank=True, null=True)
    creator = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="default_for_now")
    body = models.TextField(max_length=200, default="default_for_now")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)