# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Маршруты
"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    TodoListCreateAPIView,
)


urlpatterns = [
    path(route='auth/token/', view=obtain_auth_token, name='auth-token-get'),
    path(route='todo/', view=TodoListCreateAPIView.as_view(),
         name='todo-list-create'),
]
