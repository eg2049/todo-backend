# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Представления rest_framework.generics
"""

from rest_framework import generics

from .models import Todo
from .serializers import TodoSerializer


class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
