# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Запуск демонов
"""

from threading import Thread

from todo_backend_app.daemons.system_event_publisher_daemon import system_event_publisher_daemon


def daemon_launcher() -> None:
    """Запуск демонов сервиса
    """

    daemons = [
        system_event_publisher_daemon,
    ]

    for daemon in daemons:
        th = Thread(target=daemon, daemon=True)
        th.start()


if __name__ == '__main__':
    pass
