import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")

    RABBITMQ_HOST = os.getenv(
        "RABBITMQ_HOST",
        "localhost",
    )

    RABBITMQ_PORT = int(
        os.getenv("RABBITMQ_PORT", "5672")
    )

    RABBITMQ_USER = os.getenv(
        "RABBITMQ_USER",
        "guest",
    )

    RABBITMQ_PASSWORD = os.getenv(
        "RABBITMQ_PASSWORD",
        "guest",
    )

    RABBITMQ_QUEUE = os.getenv(
        "RABBITMQ_QUEUE",
        "email_queue",
    )

    SMTP_HOST = os.getenv(
        "SMTP_HOST",
        "localhost",
    )

    SMTP_PORT = int(
        os.getenv("SMTP_PORT", "1025")
    )

    SMTP_USERNAME = os.getenv(
        "SMTP_USERNAME"
    )

    SMTP_PASSWORD = os.getenv(
        "SMTP_PASSWORD"
    )

    EMAIL_FROM = os.getenv(
        "EMAIL_FROM",
        "noreply@example.com",
    )


settings = Settings()