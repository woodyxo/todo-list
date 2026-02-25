import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Modelo base abstrato com campos comuns.
    Todos os modelos devem herdar deste para padronização.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['modified_at']),
            models.Index(fields=['is_active']),
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"


class User(BaseModel):
    """Representa os membros do board (sem relação com o auth do Django)."""
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name


class Tag(BaseModel):
    """Rótulos livres para categorizar tarefas."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Task(BaseModel):
    """Modelo principal — representa uma tarefa do board."""

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='todo',
    )
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default='medium',
    )
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
    )
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtasks',
    )
    tags = models.ManyToManyField(Tag, through='TaskTag', blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
        ]

    def __str__(self):
        return self.title


class TaskTag(models.Model):
    """Tabela intermediária explícita entre Task e Tag."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'tag')
        verbose_name_plural = 'Task Tags'

    def __str__(self):
        return f"{self.task.title} - {self.tag.name}"
