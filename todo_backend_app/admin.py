# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Панель администратора
"""

from django.contrib import admin

from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    """
    Отображение модели Todo
    """
    list_display = ('id', 'owner', 'title', 'description',
                    'done', 'created_date', 'modified_date', 'version', )
    list_display_links = ('id', 'title', )
    search_fields = ('id', 'title', 'description', )
    list_editable = ('done', )
    list_filter = ('owner', 'done', )


admin.site.register(Todo, TodoAdmin)
