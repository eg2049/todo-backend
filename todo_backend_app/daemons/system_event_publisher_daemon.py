# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Демон публикации событий kafka
"""

import time
from datetime import datetime

import requests

from todo_backend_app.kafka.producer import event_sender
from config.config import LOCAL_HOST_HTTP, SERVICE_PORT


def system_event_publisher_daemon() -> None:
    """Демон публикации событий kafka
    """

    while True:

        try:
            response = requests.get(
                url=f'{LOCAL_HOST_HTTP}:{SERVICE_PORT}/api/v1/kafka/event/get/'
            )

            if response.status_code == 200 and response.json():

                for event in response.json():

                    event_sender(
                        topic=event.get('topic'),
                        value=event.get('payload')
                    )

                    # проставление инстансу модели SystemEvent published_date после того как событе было опубликовано
                    r = requests.put(
                        url=f'{LOCAL_HOST_HTTP}:{SERVICE_PORT}/api/v1/kafka/event/update/{event.get("pk")}/',
                        json={
                            'event_id': event.get('event_id'),
                            'topic': event.get('topic'),
                            'payload': event.get('payload'),
                            'published_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                        }
                    )

                    if r.status_code != 200:
                        pass

            else:
                pass

        except requests.exceptions.ConnectionError:
            pass

        time.sleep(5)


if __name__ == '__main__':
    pass
