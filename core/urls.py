from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.viewsets import UserViewSet, TagViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
