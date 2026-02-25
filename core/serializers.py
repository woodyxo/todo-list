from rest_framework import serializers

from core.models import Task, Tag, TaskTag, User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User."""

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_active', 'created_at', 'modified_at']
        read_only_fields = ['id', 'created_at', 'modified_at']


class TagSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Tag."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'is_active', 'created_at', 'modified_at']
        read_only_fields = ['id', 'created_at', 'modified_at']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer de leitura para Task — exibe nomes de tags e do usuário atribuído."""
    tags = TagSerializer(many=True, read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'assigned_to', 'parent_task',
            'tags', 'is_active', 'created_at', 'modified_at',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']
