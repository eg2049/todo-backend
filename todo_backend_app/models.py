# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Модели
"""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Модель профиля пользователя
    """

    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name='profile', verbose_name='Профиль')

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    modified_date = models.DateTimeField(
        auto_now=True, verbose_name='Дата редактирования')

    version = models.PositiveIntegerField(default=0, verbose_name='Версия')

    class Meta:
        """Дополнительные параметры модели
        """

        # отображение кириллицей
        verbose_name = 'Профиль'

        # отображение кириллицей во множественном числе
        verbose_name_plural = 'Профили'

        # сортировка инстансов модели
        ordering = ('created_date', 'user', )

    def __str__(self) -> str:
        """Строковое отображение инстанса модели

        Returns:
            str: строковое отображение инстанса модели
        """

        return self.user.__str__()

    def save(self, *args, **kwargs) -> None:
        """Действия при сохранении инстанса модели
        """

        # изменение версии при редактировании
        self.version += 1

        # сохранение инстанса модели при помощи super()
        super().save(*args, **kwargs)


class Todo(models.Model):
    """Модель задачи
    """

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,
                              null=True, related_name='todo_owner', verbose_name='Владелец')

    title = models.CharField(max_length=255, null=True,
                             db_index=True, verbose_name='Заголовок')

    description = models.TextField(
        blank=True, null=True, db_index=True, verbose_name='Описание')

    done = models.BooleanField(default=False, verbose_name='Выполнено')

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    modified_date = models.DateTimeField(
        auto_now=True, verbose_name='Дата редактирования')

    version = models.PositiveIntegerField(default=0, verbose_name='Версия')

    class Meta:
        """Дополнительные параметры модели
        """

        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('created_date', 'title', 'description', )

    def __str__(self) -> str:
        """Строковое отображение инстанса модели

        Returns:
            str: строковое отображение инстанса модели
        """

        return self.title

    def save(self, *args, **kwargs) -> None:
        """Действия при сохранении инстанса модели
        """

        self.version += 1

        super().save(*args, **kwargs)


if __name__ == '__main__':
    pass
