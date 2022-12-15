from django.apps import AppConfig


class TodoBackendAppConfig(AppConfig):
    """Конфигурация приложения
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_backend_app'
    verbose_name = 'Todo App'
