# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Представления rest_framework.generics
"""

from django.contrib.auth.models import User

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from todo_backend_app.mixins import LoginMixin, ProfileMixin, LogoutMixin, UserMixin
from todo_backend_app.models import Profile, Todo
from todo_backend_app.serializers import ProfileSerializer, TodoSerializer, UserSerializer


class LoginAPIView(LoginMixin, ObtainAuthToken):
    """Представление для обработки запроса на аутентификацию
    """

    # разрешения необходимые для аутентификации
    permission_classes = [
        permissions.AllowAny,
    ]


class LogoutAPIView(LogoutMixin, generics.GenericAPIView):
    """Представление для обработки запроса на деаутентификацию
    """

    # разрешения необходимые для деаутентификации
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class TodoListCreateAPIView(generics.ListCreateAPIView):
    """Представление для обработки запроса 
    на создание инстанса модели Todo 
    и получение списка инстансов модели Todo
    """

    # список с инстансами модели Todo
    queryset = Todo.objects.all()

    # класс сериализатор модели Todo
    serializer_class = TodoSerializer

    # разрешения необходимые для создания инстанса Todo и получение списка инстансов Todo
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class UserDetailAPIView(UserMixin, generics.RetrieveAPIView):
    """Представление для обработки запроса на получение данных пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # разрешения необходимые для получения данных пользователя
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class UserRegistrationAPIView(UserMixin, generics.CreateAPIView):
    """Представление для обработки запроса на регистрацию пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # разрешения необходимые для регистрации
    permission_classes = [
        permissions.AllowAny,
    ]


class ProfileAPIView(ProfileMixin, generics.GenericAPIView):
    """Представление для обработки запросов связанных с профилем пользователя
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [
        permissions.AllowAny,
    ]


if __name__ == '__main__':
    pass
