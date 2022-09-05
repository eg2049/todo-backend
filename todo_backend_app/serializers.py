# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Сериализаторы
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, Todo
from .validators import unique_email


class TodoSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Todo
    """

    class Meta:
        model = Todo
        fields = [
            'pk',
            'owner',
            'title',
            'description',
            'done',
            'created_date',
            'modified_date',
            'version',
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User
    """
    password = serializers.CharField(write_only=True)
    profile_data = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = User

        fields = [
            'pk',
            'username',
            'password',
            'email',
            'last_name',
            'first_name',
            'profile_data',
        ]

        extra_kwargs = {
            'email': {
                'validators': [
                    unique_email,
                ]
            }
        }

    def get_profile_data(self, obj):
        result = {
            'created_date': obj.profile.created_date,
            'modified_date': obj.profile.modified_date,
            'version': obj.profile.version,
        }

        return result

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )

        user.set_password(validated_data.get('password'))
        user.save()

        Profile.objects.create(
            user=user
        )

        return user
