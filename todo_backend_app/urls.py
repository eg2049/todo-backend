# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Контроллеры
"""

from django.urls import path

from todo_backend_app.views import (
    LoginAPIView,
    LogoutAPIView,
    SystemEventAPIView,
    TodoListCreateAPIView,
    ProfileAPIView,
    UserDetailAPIView,
    UserRegistrationAPIView,
)

# список с endpoint-ами и обрабатывающими их представлениями
urlpatterns = [
    path(route='auth/token/get/',
         view=LoginAPIView.as_view(), name='auth-token-get'),

    path(route='auth/token/remove/', view=LogoutAPIView.as_view(),
         name='auth-token-remove'),

    path(route='profile/',
         view=UserDetailAPIView.as_view(), name='profile'),

    path(route='profile/confirmation/',
         view=ProfileAPIView.as_view(), name='profile-confirmation'),

    path(route='registration/',
         view=UserRegistrationAPIView.as_view(), name='registration'),

    path(route='kafka/event/create/', view=SystemEventAPIView.as_view(),
         name='system-event-create'),

    path(route='todo/', view=TodoListCreateAPIView.as_view(),
         name='todo-list-create'),
]


if __name__ == '__main__':
    pass
