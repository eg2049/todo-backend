# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Миксины
"""

from datetime import datetime
from uuid import UUID, uuid4

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from todo_backend_app.error_messages import error_message_get_auth, error_message_get_common, error_message_get_todo
from todo_backend_app.models import Profile, SystemEvent, Todo
from todo_backend_app.utils import email_regex

from config.config import CONFIRM_ACCOUNT_URL, PASSWORD_MIN_LENGTH, TODO_UI_HOST


class LoginMixin():
    """Миксин для обработки запроса на аутентификацию
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Переопределение метода обрабатывающего POST запрос

        Args:
            request (Request): HTTP request

        Returns:
            Response: HTTP response
        """

        # попытка выполнить успешную аутентификацию при помощи super()
        try:
            return super().post(request, *args, **kwargs)

        # обработка исключения
        except ValidationError as exc:

            username = request.data.get('username')
            profile = Profile.objects.filter(user__username=username)

            # проверка подтверждённости профиля
            if profile and not profile[0].confirmed_date:
                response_status = status.HTTP_400_BAD_REQUEST
                error_message = error_message_get_auth(
                    message_name='profile_not_confirmed')

            # проверка правильности логина / пароля
            elif exc.detail.get('non_field_errors') or exc.detail.get('password'):
                response_status = status.HTTP_400_BAD_REQUEST
                error_message = error_message_get_auth(
                    message_name='invalid_credentials')

            # 500 ответ
            else:
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_message = None

            return Response(
                data={
                    'status': response_status,
                    'message': error_message
                },
                status=response_status
            )


class LogoutMixin():
    """Миксин для обработки запроса на деаутентификацию
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Переопределение метода обрабатывающего POST запрос

        Args:
            request (Request): HTTP request

        Returns:
            Response: HTTP response
        """

        # удаление токена аутентификации
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)


class TodoMixin():
    """Миксин для обработки запросов связанных с инстансами модели Todo
    """

    # название поля модели Todo к которому привязан инстанс модели User
    user_field = 'owner'

    # можно ли администратору или персоналу работать со всеми todo
    allow_staff_permissions = False

    def create(self, request: Request, *args, **kwargs) -> Response or ValidationError or APIException:
        """Переопределение метода создания инстанса модели Todo

        Args:
            request (Request): HTTP request

        Raises:
            ValidationError: title уже существует для пользователя
            ValidationError: title - пустая строка или None
            APIException: 500 ответ

        Returns:
            Response: HTTP response
        """

        # заполнение поля owner инстанса модели Todo пользователем который делает запрос
        if not request.data.get('owner'):
            request.data['owner'] = request.user.pk

        # поытка создать инстанс модели Todo при помощи super()
        try:
            return super().create(request, *args, **kwargs)

        # обработка ошибок при валидации
        except ValidationError:

            title = request.data.get('title')

            # проверка уникальности title для пользователя
            if self.queryset.filter(owner=request.user, title=title):
                raise ValidationError(
                    detail={
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': error_message_get_todo(message_name='title_already_exists')
                    },
                    code=status.HTTP_400_BAD_REQUEST
                )

            # проверка валидности title
            elif title == '' or title is None:
                raise ValidationError(
                    detail={
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': error_message_get_todo(message_name='title_is_empty')
                    },
                    code=status.HTTP_400_BAD_REQUEST
                )

            # 500 ответ
            else:
                raise APIException(
                    detail={
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': error_message_get_common(message_name='internal_server_error')
                    },
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def get_object(self, *args, **kwargs) -> Todo or PermissionDenied:
        """Переопределение метода получения отдельного инстанса модели Todo

        Raises:
            PermissionDenied: пользователь не имеет прав на работу с инстансом модели Todo

        Returns:
            Todo: инстанс модели Todo или исключение
        """

        # определение пользователя, который делает запрос
        user = self.request.user

        # получение инстанса модели Todo
        obj = super().get_object(*args, **kwargs)

        # если пользователь - владелец инстанса модели Todo или пользователь имеет роль администратора или персонала
        # и администратору или персоналу можно получать все инстансы модели Todo
        if (obj.owner == user) or (self.allow_staff_permissions and user.is_staff):
            return obj

        else:
            raise PermissionDenied(
                detail={
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': error_message_get_common(message_name='forbidden'),
                    'todo_id': obj.id
                },
                code=status.HTTP_403_FORBIDDEN
            )

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Переопределение метода получения списка инстансов модели Todo

        Returns:
            QuerySet: список инстансов модели Todo
        """

        user = self.request.user

        # все инстансы модели Todo
        queryset = super().get_queryset(*args, **kwargs)

        # если администратору или персоналу можно получать все инстансы модели Todo
        # и пользователь имеет роль администратора или персонала
        if self.allow_staff_permissions and user.is_staff:
            result = queryset

        # если нет, через filter(), происходит поиск инстансов модели Todo принадлежащих пользователю
        else:
            lookup_data = {self.user_field: user}
            result = queryset.filter(**lookup_data)

        return result


class UserMixin():
    """Миксин для обработки запросов связанных с инстансами модели User
    """

    def post(self, request: Request, *args, **kwargs) -> Response or ValidationError or APIException:
        """Переопределение метода обрабатывающего POST запрос

        Args:
            request (Request): HTTP request

        Raises:
            ValidationError: email занят
            ValidationError: username занят
            ValidationError: пароль слишком короткий
            ValidationError: невалидный email
            APIException: 500 ответ

        Returns:
            Response: HTTP response
        """

        serializer = self.get_serializer(data=request.data)

        # если стандартные валидации drf пройдены
        if serializer.is_valid():

            # проверка уникальности email
            if User.objects.filter(email=request.data.get('email')):
                raise ValidationError(
                    detail={
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': error_message_get_auth(message_name='email_already_exists')
                    },
                    code=status.HTTP_400_BAD_REQUEST
                )

            # регистрация нового пользователя и 201 ответ
            else:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                # # суперлогика получения домена с которого происходит запрос...
                # uri = request.build_absolute_uri()
                # host = uri.split('api')[0][0:-1]

                # создание инстанса события system_event (событие kafka)
                SystemEvent.objects.create(
                    event_id=uuid4().__str__(),
                    topic='email_notification_topic',
                    payload={
                        'subject': 'account_confirmation',
                        'recipient': serializer.data.get('email'),
                        'url': f'{TODO_UI_HOST}{CONFIRM_ACCOUNT_URL}{serializer.data.get("profile_data").get("confirmation_token")}'
                    }
                )

                return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # если стандартные валидации drf не пройдены
        else:

            user = User.objects.filter(email=request.data.get(
                'email'), username=request.data.get('username'))

            # проверка существования пары email & username
            if user:

                token = Profile.objects.get(
                    user__pk=user[0].pk).confirmation_token

                SystemEvent.objects.create(
                    event_id=uuid4().__str__(),
                    topic='email_notification_topic',
                    payload={
                        'subject': 'account_confirmation',
                        'recipient': request.data.get('email'),
                        'url': f'{TODO_UI_HOST}{CONFIRM_ACCOUNT_URL}{token}'
                    }
                )

                return Response(
                    data={
                        'status': status.HTTP_200_OK
                    },
                    status=status.HTTP_200_OK
                )

            # проверка уникальности username
            elif User.objects.filter(username=request.data.get('username')):
                raise ValidationError(
                    detail={
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': error_message_get_auth(message_name='username_already_exists')
                    },
                    code=status.HTTP_400_BAD_REQUEST
                )

            # проверка валидности email
            elif not email_regex(email=request.data.get('email')):
                raise ValidationError(
                    detail={
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': error_message_get_auth(message_name='email_invalid')
                    },
                    code=status.HTTP_400_BAD_REQUEST
                )

            # 500 ответ
            else:
                raise APIException(
                    detail={
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': error_message_get_common(message_name='internal_server_error')
                    },
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """Переопределение метода получения инстанса модели User

        Args:
            request (Request): HTTP request

        Returns:
            Response: HTTP response
        """

        # получение инстанса модели User
        instance = self.queryset.get(pk=request.user.pk)

        # получение сериализатора модели User
        serializer = self.get_serializer(instance)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class ProfileMixin():
    """Миксин для работы с инстансами модели Profile
    """

    def put(self, request: Request, *args, **kwargs) -> Response or ValidationError:
        """Переопределение метода обрабатывающего PUT запрос

        Args:
            request (Request): HTTP request

        Returns:
            Response: HTTP response
        """

        token = request.data.get('token')
        token = str(token) if token else token

        password = request.data.get('password')
        password = str(password) if password else password

        try:
            UUID(token)

        # если токен не передавался, или token is None
        except TypeError:
            raise ValidationError(
                detail={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': error_message_get_auth(message_name='token_is_required')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        # если токен - не UUID
        except ValueError:
            raise ValidationError(
                detail={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': error_message_get_auth(message_name='invalid_uuid_token')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        # проверка существования токена
        if not Profile.objects.filter(confirmation_token=token):
            raise ValidationError(
                detail={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': error_message_get_auth(message_name='confirm_token_not_found')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        # проверка подтверждённости профиля
        elif Profile.objects.get(confirmation_token=token).confirmed_date:
            raise ValidationError(
                detail={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': error_message_get_auth(message_name='profile_already_confirmed')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        # если пароль не передавался или password is None
        elif not password:
            raise ValidationError(
                detail={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': error_message_get_auth(message_name='password_is_required')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        # проверка длины пароля
        elif len(password) < PASSWORD_MIN_LENGTH:
            raise ValidationError(
                detail={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': error_message_get_auth(message_name='password_too_short')
                },
                code=status.HTTP_400_BAD_REQUEST
            )

        # подтверждение профиля и установка пароля
        else:
            profile = Profile.objects.get(confirmation_token=token)
            profile.confirmed_date = datetime.now()
            profile.save()

            user = User.objects.get(profile__pk=profile.pk)
            user.set_password(raw_password=password)
            user.save()

            return Response(
                data={
                    'username': user.username
                },
                status=status.HTTP_200_OK
            )


if __name__ == '__main__':
    pass
