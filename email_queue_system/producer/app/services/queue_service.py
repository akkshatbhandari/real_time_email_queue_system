import json

import pika

from ..config import settings


class QueueService:

    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.username = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.queue = settings.RABBITMQ_QUEUE

    def _create_connection(self):

        credentials = pika.PlainCredentials(
            self.username,
            self.password,
        )

        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=60,
            blocked_connection_timeout=30,
        )

        return pika.BlockingConnection(parameters)

    def publish(self, message: dict):

        connection = self._create_connection()

        try:
            channel = connection.channel()

            channel.queue_declare(
                queue=self.queue,
                durable=True,
            )

            channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                ),
            )

        finally:
            connection.close()