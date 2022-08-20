# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Маршруты
"""

from django.urls import path

from .views import (
    TodoListCreateAPIView,
)


urlpatterns = [
    path(route='todo/', view=TodoListCreateAPIView.as_view(), name='todo-list-create')
]
