import pika

from .config import settings


class RabbitMQConsumer:

    def __init__(self):

        self.connection = None
        self.channel = None

    def connect(self):

        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASSWORD,
        )

        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials,
            heartbeat=60,
            blocked_connection_timeout=30,
        )

        self.connection = (
            pika.BlockingConnection(
                parameters
            )
        )

        self.channel = (
            self.connection.channel()
        )

        self.channel.queue_declare(
            queue=settings.RABBITMQ_QUEUE,
            durable=True,
        )

        # Process one message at a time.
        self.channel.basic_qos(
            prefetch_count=1
        )

    def close(self):

        if self.connection:

            self.connection.close()