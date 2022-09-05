# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Представления rest_framework.viewsets
"""

from rest_framework import permissions, viewsets

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    Представление модели Todo
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = 'pk'

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
