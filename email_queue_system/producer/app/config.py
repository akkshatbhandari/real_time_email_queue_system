import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")

    # RabbitMQ
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))

    RABBITMQ_USER = os.getenv(
        "RABBITMQ_USER",
        "guest"
    )

    RABBITMQ_PASSWORD = os.getenv(
        "RABBITMQ_PASSWORD",
        "guest"
    )

    RABBITMQ_QUEUE = os.getenv(
        "RABBITMQ_QUEUE",
        "email_queue"
    )

    RABBITMQ_RETRY_QUEUE = os.getenv(
        "RABBITMQ_RETRY_QUEUE",
        "email_retry_queue"
    )

    RABBITMQ_DLQ = os.getenv(
        "RABBITMQ_DLQ",
        "email_dead_letter_queue"
    )

    # SMTP
    SMTP_HOST = os.getenv(
        "SMTP_HOST",
        "localhost"
    )

    SMTP_PORT = int(
        os.getenv("SMTP_PORT", "1025")
    )

    EMAIL_FROM = os.getenv(
        "EMAIL_FROM",
        "noreply@example.com"
    )

    # S3
    S3_ENDPOINT_URL = os.getenv(
        "S3_ENDPOINT_URL"
    )

    S3_ACCESS_KEY = os.getenv(
        "S3_ACCESS_KEY"
    )

    S3_SECRET_KEY = os.getenv(
        "S3_SECRET_KEY"
    )

    S3_BUCKET_NAME = os.getenv(
        "S3_BUCKET_NAME"
    )

    S3_REGION = os.getenv(
        "S3_REGION",
        "auto"
    )


settings = Settings()