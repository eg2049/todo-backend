# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Валидаторы
"""

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


unique_email = UniqueValidator(queryset=User.objects.all(
), message='A user with that email already exists.', lookup='iexact')
