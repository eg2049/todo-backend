# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Маршруты
"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    LogoutAPIView,
    UserDetailAPIView,
    UserRegistrationAPIView,
    TodoListCreateAPIView,
)


urlpatterns = [
    path(route='profile/',
         view=UserDetailAPIView.as_view(), name='profile'),
    path(route='registration/',
         view=UserRegistrationAPIView.as_view(), name='registration'),
    path(route='auth/token/get/', view=obtain_auth_token, name='auth-token-get'),
    path(route='auth/token/remove/', view=LogoutAPIView.as_view(),
         name='auth-token-remove'),
    path(route='todo/', view=TodoListCreateAPIView.as_view(),
         name='todo-list-create'),
]
