# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Маршрутизаторы
"""

from rest_framework import routers

from todo_backend_app.viewsets import TodoViewSet


# создание маршрутизатора
router = routers.DefaultRouter()

# регистрация маршрута (endpoint-а) "/todo/"
router.register(prefix='todo', viewset=TodoViewSet, basename='todo')

# список с endpoint-ами и обрабатывающими их представления
urlpatterns = router.urls
