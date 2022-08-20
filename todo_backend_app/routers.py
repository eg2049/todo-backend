# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Маршрутизаторы
"""

from rest_framework import routers

from .viewsets import TodoViewSet


router = routers.DefaultRouter()
router.register(prefix='todo', viewset=TodoViewSet, basename='todo')


urlpatterns = router.urls
