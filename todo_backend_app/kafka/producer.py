# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Kafka producer
"""

import json

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

from config.config import KAFKA_BROKERS


def json_serializer(data: dict) -> bytes:
    """Сериализатор отправляемых kafka-событий

    Args:
        data (dict): данные события

    Returns:
        bytes: json-поток байт
    """

    return json.dumps(obj=data).encode(encoding='utf-8')


def topic_exists_checker(topic: str) -> bool:
    """Проверка существования топика

    Args:
        topic (str): название топика

    Returns:
        bool: существует ли топик
    """

    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKERS
    )

    topic_list = admin_client.list_topics()

    return topic in topic_list


def topic_creator(name: str, num_partitions: int = 1, replication_factor: int = 1) -> None:
    """Создание нового топика

    Args:
        name (str): название топика
        num_partitions (int, optional): количество партиций топика. Defaults to 1.
        replication_factor (int, optional): количество реплик топика. Defaults to 1.
    """

    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKERS
    )

    new_topic = NewTopic(name=name, num_partitions=num_partitions,
                         replication_factor=replication_factor)

    try:
        admin_client.create_topics(
            new_topics=[
                new_topic
            ]
        )

    except TopicAlreadyExistsError:
        pass


def producer_creator() -> KafkaProducer:
    """Создание инстанса KafkaProducer

    Returns:
        KafkaProducer: инстанс KafkaProducer
    """

    producer = KafkaProducer(

        # адреса брокеров
        bootstrap_servers=KAFKA_BROKERS,

        # сериализатор для событий
        value_serializer=json_serializer,
    )

    return producer


def event_sender(topic: str, value: dict) -> None:
    """Отправка событий

    Args:
        topic (str): топик в который нужно отправить событие
        value (dict): событие
    """

    producer = producer_creator()

    # т.к. при создании инстанса producer-а в value_serializer передавался json_serializer()
    # при отправке события этот сериализатор будет использоваться автоматически
    producer.send(
        topic=topic,
        value=value
    )


if __name__ == '__main__':
    pass
