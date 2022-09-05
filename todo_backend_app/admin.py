# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Панель администратора
"""

from django.contrib import admin

from .models import Profile, Todo


class ProfileAdmin(admin.ModelAdmin):
    """
    Отображение модели Profile
    """
    list_display = ('id', 'user', 'created_date', 'modified_date', 'version', )
    list_display_links = ('id', 'user', )
    search_fields = ('id', 'user', )


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
admin.site.register(Profile, ProfileAdmin)
