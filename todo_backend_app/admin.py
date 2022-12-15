# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Панель администратора
"""

from django.contrib import admin

from todo_backend_app.models import Profile, Todo


class ProfileAdmin(admin.ModelAdmin):
    """Отображение модели Profile в панели администратора
    """

    # поля которые будут оторбражаться в реестре панели администратора
    list_display = (
        'id',
        'user',
        'created_date',
        'modified_date',
        'version',
    )

    # поля которые будут ссылками в реестре панели администратора
    list_display_links = (
        'id',
        'user',
    )

    # поля по которым можно искать нужный инстанс в реестре панели администратора
    search_fields = (
        'id',
        'user',
    )


class TodoAdmin(admin.ModelAdmin):
    """Отображение модели Todo в панели администратора
    """

    list_display = (
        'id',
        'owner',
        'title',
        'description',
        'done',
        'created_date',
        'modified_date',
        'version',
    )

    list_display_links = (
        'id',
        'title',
    )

    search_fields = (
        'id',
        'title',
        'description',
    )

    # поля которые можно изменять находясь в реестре панели администратора
    list_editable = (
        'done',
    )

    # поля по которым можно будет фильтроваться находясь в реестре панели администратора
    list_filter = (
        'owner',
        'done',
    )


# подключение моделей в панель администратора
admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile, ProfileAdmin)
