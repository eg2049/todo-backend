# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Представления rest_framework.generics
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import TodoSerializer


class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]


class LogoutAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
