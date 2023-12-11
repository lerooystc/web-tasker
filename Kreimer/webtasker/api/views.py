import rest_framework.permissions as perms
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import generics, status
from .serializers import *
from .models import Board, Column, Task, Note
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.select_related('id_user').prefetch_related('members', 'notes', 'columns', 'columns__tasks',
                                                                        'columns__tasks__notes')
    serializer_class = BoardSerializer
    create_serializer_class = CreateBoardSerializer

    def create(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.create_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.data.get('title')
            description = serializer.data.get('description')
            id_user = self.request.user
            queryset = Board.objects.filter(id_user=id_user)
            if queryset.count() > 2:
                return Response({'Bad Request': 'Too many boards already exist...'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                board = Board(id_user=id_user, title=title,
                              description=description)
                board.save()
                board.members.add(id_user)
                board.save()
                self.request.session['board_invite_code'] = board.invite_code
                return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.prefetch_related('tasks', 'tasks__notes')
    serializer_class = ColumnSerializer
    create_serializer_class = CreateColumnSerializer

    def create(self, request):
        serializer = self.create_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.data.get('title')
            number = serializer.data.get('number')
            id_board = serializer.data.get('id_board')
            board = get_object_or_404(Board, pk=id_board)
            queryset = Column.objects.filter(id_board=id_board)
            if queryset.count() > 9:
                return Response({'Bad Request': 'Too many columns already exist...'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                column = Column(id_board=board, title=title, number=number)
                column.save()
                return Response(ColumnSerializer(column).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related('notes')
    serializer = TaskSerializer
    create_serializer_class = CreateTaskSerializer

    def create(self, request):
        serializer = self.create_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            id_column = serializer.data.get('id_column')
            title = serializer.data.get('title')
            body = serializer.data.get('body')
            color = serializer.data.get('color')
            priority = serializer.data.get('priority')
            finish_by = serializer.data.get('finish_by')
            column = get_object_or_404(Column, pk=id_column)
            queryset = Task.objects.filter(id_column=column)
            if queryset.count() > 19:
                return Response({'Bad Request': 'Too many tasks already exist...'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                task = Task(id_column=column, title=title, body=body, color=color, priority=priority,
                            finish_by=finish_by)
                task.save()
                return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.select_related('creator')
    serializer_class = NoteSerializer
    create_serializer_class = CreateNoteSerializer

    def create(self, request):
        serializer = self.create_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if board := serializer.data.get('id_board'):
                id_board = get_object_or_404(Board, pk=board)
                id_task = None
                flag = 'board'
            if task := serializer.data.get('id_task'):
                id_task = get_object_or_404(Task, pk=task)
                id_board = None
                flag = 'task'
            title = serializer.data.get('title')
            body = serializer.data.get('body')
            id_user = self.request.user
            queryset = Note.objects.filter(id_board=id_board) if flag == 'board' else Note.objects.filter(
                id_task=id_task)
            if queryset.count() > 29:
                return Response({'Bad Request': 'Too many notes already exist...'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                note = Note(id_board=id_board, id_task=id_task, creator=id_user, title=title, body=body)
                note.save()
                return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserBoards(generics.ListAPIView):
    permission_classes = [perms.IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request):
        host = self.request.user
        queryset = Board.objects.filter(id_user=host)
        serializer = UserBoardsSerializer(queryset, many=True)
        return Response(serializer.data)


class UserRegister(APIView):
    permission_classes = [perms.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [perms.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(request.data)
            login(request, user)
            return Response({"Token": Token.objects.get_or_create(user=user)[0].key}, status=status.HTTP_200_OK)


class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [perms.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UsernameTaken(APIView):
    permission_classes = [perms.AllowAny]
    serializers = UsernameSerializer

    def post(self, request):
        serializer = UsernameSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"Username valid": "Username valid."}, status=status.HTTP_200_OK)
        return Response({'Username taken': 'User already exists...'}, status=status.HTTP_400_BAD_REQUEST)

