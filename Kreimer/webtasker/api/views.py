from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import generics, status
from .serializers import BoardSerializer, ColumnSerializer, TaskSerializer, CreateBoardSerializer,\
    CreateColumnSerializer, CreateTaskSerializer
from .models import Board, Column, Task
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class BoardView(generics.ListAPIView):
    queryset = Board.objects.select_related('id_user').prefetch_related('members', 'columns', 'columns__tasks')
    serializer_class = BoardSerializer


class CreateBoardView(APIView):
    serializer_class = CreateBoardSerializer

    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
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


class CreateColumnView(APIView):
    serializer_class = CreateColumnSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
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


class CreateTaskView(APIView):
    serializer_class = CreateTaskSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
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


class GetColumnTasks(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        column = self.request.query_params.get('column')
        if column:
            queryset = get_list_or_404(Task, id_column=column)
            serializer = TaskSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'Bad Request': 'Please pass the parameter'}, status=status.HTTP_400_BAD_REQUEST)


class GetBoardColumns(generics.ListAPIView):
    queryset = Column.objects.prefetch_related('tasks')
    serializer_class = ColumnSerializer

    def list(self, request):
        board = self.request.query_params.get('board')
        if board:
            queryset = get_list_or_404(Column.objects.prefetch_related('tasks'), id_board=board)
            serializer = ColumnSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'Bad Request': 'Please pass the parameter'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserBoards(generics.ListAPIView):
    queryset = Board.objects.select_related('id_user').prefetch_related('members', 'columns', 'columns__tasks')
    serializer_class = BoardSerializer

    def list(self, request):
        if request.user.is_authenticated:
            host = self.request.user
            queryset = Board.objects.filter(id_user=host).select_related('id_user').prefetch_related(
                'members', 'columns', 'columns__tasks')
            serializer = BoardSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'Unauthorized': 'Please log in!'}, status=status.HTTP_401_UNAUTHORIZED)
