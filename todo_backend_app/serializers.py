# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Сериализаторы
"""

from uuid import uuid4

from django.contrib.auth.models import User
from rest_framework import serializers

from todo_backend_app.models import Profile, SystemEvent, Todo

# # не используется, пояснения в todo_backend_app.validators
# from todo_backend_app.validators import unique_email, unique_username


class TodoSerializer(serializers.ModelSerializer):
    """Сериализатор модели Todo
    """

    class Meta:
        """Подключение модели которую необходимо сериализовывать
        """

        # модель
        model = Todo

        # список полей модели которые необходимо сериализовывать
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

        # валидаторы
        validators = [

            serializers.UniqueTogetherValidator(
                queryset=Todo.objects.all(),
                fields=('owner', 'title'),
                message='Some custom message.'
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User
    """

    # password = serializers.CharField(write_only=True)
    profile_data = serializers.SerializerMethodField(read_only=False)

    class Meta:
        """Подключение модели которую необходимо сериализовывать
        """

        model = User

        fields = [
            'pk',
            'username',
            # 'password',
            'email',
            'last_name',
            'first_name',
            'profile_data',
        ]

        # дополнительные параметры при работе с полями модели
        # валидаторы не используется, пояснения в todo_backend_app.validators
        extra_kwargs = {

            # 'email': {
            #     'validators': [
            #         unique_email,
            #     ]
            # },
            # 'username': {
            #     'validators': [
            #         unique_username,
            #     ]
            # }

        }

    def get_profile_data(self, obj: User) -> dict:
        """Получение данных инстанса модели Profile привзянного к инстансу модели User  

        Args:
            obj (User): инстанс модели User

        Returns:
            dict: данные инстанса модели Profile привязанного к инстансу модели User
        """

        result = {
            'confirmation_token': obj.profile.confirmation_token,
            'created_date': obj.profile.created_date,
            'modified_date': obj.profile.modified_date,
            'version': obj.profile.version,
        }

        return result

    def create(self, validated_data: dict) -> User:
        """Создание нового пользователя

        Args:
            validated_data (dict): данные создаваемого инстанса модели User

        Returns:
            User: инстанс модели User
        """

        # создание инстанса модели User
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )

        # # сохранение пароля в зашифрованном виде
        # user.set_password(validated_data.get('password'))
        # user.save()

        # создание инстанса модели Profile для нового инстанса модели User
        Profile.objects.create(
            user=user,
            confirmation_token=uuid4().__str__()
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор модели Profile
    """

    class Meta:
        """Подключение модели которую необходимо сериализовывать
        """

        model = Profile

        fields = [
            'confirmation_token',
            'confirmed_date',
        ]

    # def update(self, instance: Profile, validated_data: dict) -> Profile:
    #     """Редактирование инстанса модели Profile

    #     Args:
    #         instance (Profile): инстанс модели Profile
    #         validated_data (dict): данные для редактирования

    #     Returns:
    #         Profile: инстанс модели Profile
    #     """

    #     # проставление даты подтверждения акканута, если она ещё не проставлена
    #     if not instance.confirmed_date:
    #         instance.confirmed_date = datetime.now()

    #     obj = super().update(instance=instance, validated_data=validated_data)

    #     return obj


if __name__ == '__main__':
    pass
