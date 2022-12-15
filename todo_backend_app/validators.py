# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Валидаторы
"""

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from todo_backend_app.error_messages import error_message_get_auth


# валидатор уникальности email
# не используется т.к. не понятно как редактировать возвращаемое тело
unique_email = UniqueValidator(
    queryset=User.objects.all(),
    message=error_message_get_auth(message_name='email_already_exists'),
    lookup='iexact'
)

# валидатор уникальности username
# не используется т.к. не понятно как редактировать возвращаемое тело
unique_username = UniqueValidator(
    queryset=User.objects.all(),
    message=error_message_get_auth(message_name='username_already_exists'),
    lookup='iexact'
)

if __name__ == '__main__':
    pass
