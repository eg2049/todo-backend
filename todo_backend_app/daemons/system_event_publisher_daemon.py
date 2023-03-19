# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Демон публикации событий kafka
"""

from datetime import datetime
from time import sleep

from django.db.utils import ProgrammingError

from todo_backend_app.kafka.producer import event_sender
from todo_backend_app.models import SystemEvent


def system_event_publisher_daemon() -> None:
    """Демон публикации событий kafka
    """

    while True:

        try:
            not_published_events = SystemEvent.objects.filter(
                published_date=None)

            for event in not_published_events:

                event_sender(
                    topic=event.topic,
                    value=event.payload
                )

                event.published_date = datetime.now()

                event.save()

        except ProgrammingError:
            pass

        sleep(5)


if __name__ == '__main__':
    pass
