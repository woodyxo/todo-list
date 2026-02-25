from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from core.models import Task, Tag, User
from core.serializers import TaskSerializer, TagSerializer, UserSerializer
from core.request_serializers import TaskCreateUpdateSerializer
from core.filters import TaskFilter, TagFilter, UserFilter


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Users (CRUD completo)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar Tags (CRUD completo)."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Tasks (CRUD completo).

    Endpoints extras:
    - GET /api/tasks/{id}/subtasks/ — listar subtarefas
    """
    queryset = Task.objects.all().prefetch_related('tags').select_related('assigned_to')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'modified_at', 'priority', 'due_date']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Retorna serializer diferente para criar/atualizar."""
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer

    @action(detail=True, methods=['get'])
    def subtasks(self, request, pk=None):
        """
        Listar subtarefas de uma tarefa.

        GET /api/tasks/{id}/subtasks/
        Retorna apenas as tasks cujo parent_task == id informado.
        """
        task = self.get_object()
        subtasks = Task.objects.filter(parent_task=task).prefetch_related('tags').select_related('assigned_to')
        serializer = TaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
