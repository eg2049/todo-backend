# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Демон публикации событий kafka
"""

import time
from datetime import datetime

from todo_backend_app.kafka.producer import event_sender
from todo_backend_app.models import SystemEvent


def system_event_publisher_daemon() -> None:
    """Демон публикации событий kafka
    """

    while True:

        not_published_events = SystemEvent.objects.filter(
            published_date=None)

        for event in not_published_events:

            event_sender(
                topic=event.topic,
                value=event.payload
            )

            event.published_date = datetime.now()

            event.save()

        time.sleep(5)


if __name__ == '__main__':
    pass
