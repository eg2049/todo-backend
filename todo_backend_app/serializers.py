# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Сериализаторы
"""

from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Todo
    """

    class Meta:
        model = Todo
        fields = (
            'pk',
            'owner',
            'title',
            'description',
            'done',
            'created_date',
            'modified_date',
            'version',
        )
