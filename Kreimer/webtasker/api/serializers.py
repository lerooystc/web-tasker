from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from .models import Board, Column, Task, Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id_board', 'id_task', 'creator', 'title', 'body')


class TaskSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'id_column', 'title', 'body', 'color', 'priority', 'finish_by', 'taken_by', 'notes')


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
    notes = NoteSerializer(many=True, read_only=True)
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'id_user', 'members', 'title', 'description', 'columns',
                  'invite_code', 'created_at', 'notes')


class CreateBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('title', 'description')


class UserBoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'title', 'description')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_obj = User.objects.create_user(email=validated_data['email'], username=validated_data['username'],
                                            password=validated_data['password'])
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise ValidationError('User not found.')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

