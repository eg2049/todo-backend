# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Представления rest_framework.viewsets
"""

from rest_framework import permissions, viewsets

from todo_backend_app.mixins import TodoMixin
from todo_backend_app.models import Todo
from todo_backend_app.serializers import TodoSerializer


class TodoViewSet(TodoMixin, viewsets.ModelViewSet):
    """Представление модели Todo
    """

    # список с инстансами модели Todo
    queryset = Todo.objects.all()

    # класс сериализатор модели Todo
    serializer_class = TodoSerializer

    # поле по которому происходит идентификация инстанса Todo
    lookup_field = 'pk'

    # разрешения необходимые при работе с инстансами Todo
    permission_classes = [
        permissions.IsAuthenticated,
    ]


if __name__ == '__main__':
    pass
