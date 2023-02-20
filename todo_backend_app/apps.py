from django.apps import AppConfig


class TodoBackendAppConfig(AppConfig):
    """Конфигурация приложения
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_backend_app'
    verbose_name = 'Todo App'

    def ready(self) -> None:
        """Судя по всему здесь можно прописать операции которые будут выполняться когда "основное" приложение уже запустилось

        какие-то кастомные миграции с добавлением каких-то записей в таблицы (вне того что есть в models.py)
        запуск демонов 
        ...

        """

        # выглядит так себе, но работает, позволяя импортировать модели внутри модулей демонов
        from todo_backend_app.daemons.daemon_launcher import daemon_launcher

        # запус демонов перед запуском "основного" приложения
        daemon_launcher()

        return super().ready()


if __name__ == '__main__':
    pass
