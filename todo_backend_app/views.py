# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Представления rest_framework.generics
"""

from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import TodoSerializer, UserSerializer


class LogoutAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=request.user.pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        permissions.AllowAny,
    ]
