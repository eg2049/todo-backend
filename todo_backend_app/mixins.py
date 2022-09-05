# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Миксины
"""

from rest_framework.exceptions import PermissionDenied


class UserTodoQueryMixin():
    user_field = 'owner'
    allow_staff_permissions = False

    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super().get_object(*args, **kwargs)

        if (obj.owner == user) or (self.allow_staff_permissions and user.is_staff):
            return obj
        else:
            raise PermissionDenied(
                detail={'message': "You don't have permission to access",
                        'todo_id': obj.id}
            )

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)

        if self.allow_staff_permissions and user.is_staff:
            result = queryset
        else:
            lookup_data = {self.user_field: user}
            result = queryset.filter(**lookup_data)

        return result
