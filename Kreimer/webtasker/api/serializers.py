from rest_framework import serializers
from .models import Board, Column, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'id_column', 'title', 'body', 'color', 'priority', 'finish_by', 'taken_by')


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id_column', 'title', 'body', 'color', 'priority', 'finish_by')


class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ('id', 'id_board', 'title', 'number', 'tasks')


class CreateColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ('id_board', 'title', 'number')


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'id_user', 'members', 'title', 'description', 'columns',
                  'invite_code', 'created_at')


class CreateBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('title', 'description')





