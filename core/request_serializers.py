from rest_framework import serializers

from core.models import Task, Tag, TaskTag


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer de escrita para Task (POST / PUT / PATCH).
    Aceita tag_ids para o relacionamento M2M via through.
    """
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'assigned_to', 'parent_task',
            'tag_ids', 'is_active', 'created_at', 'modified_at',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']

    def create(self, validated_data):
        tags = validated_data.pop('tag_ids', [])
        task = Task.objects.create(**validated_data)
        for tag in tags:
            TaskTag.objects.create(task=task, tag=tag)
        return task

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            TaskTag.objects.filter(task=instance).delete()
            for tag in tags:
                TaskTag.objects.create(task=instance, tag=tag)

        return instance

    def to_representation(self, instance):
        """Retorna a representação de leitura completa após escrita."""
        from core.serializers import TaskSerializer
        return TaskSerializer(instance).data
