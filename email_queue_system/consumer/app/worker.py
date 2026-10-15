import json
from datetime import datetime, timezone

from sqlalchemy import text

from .database import SessionLocal
from .email_service import EmailService
from .rabbitmq import RabbitMQConsumer


email_service = EmailService()
rabbitmq = RabbitMQConsumer()


def process_message(
    channel,
    method,
    properties,
    body,
):

    db = SessionLocal()

    try:

        # -----------------------------
        # Parse RabbitMQ message
        # -----------------------------

        message = json.loads(
            body.decode("utf-8")
        )

        print(
            f"Received message: {message}"
        )

        email_job_id = message[
            "email_job_id"
        ]

        recipient = message[
            "recipient"
        ]

        subject = message[
            "subject"
        ]

        email_body = message[
            "body"
        ]

        # -----------------------------
        # Check current job status
        # -----------------------------

        result = db.execute(
            text(
                """
                SELECT status
                FROM email_jobs
                WHERE id = :id
                """
            ),
            {
                "id": email_job_id
            },
        )

        row = result.fetchone()

        if row is None:

            raise ValueError(
                f"Email job {email_job_id} "
                "does not exist"
            )

        current_status = row[0]

        # -----------------------------
        # Idempotency
        # -----------------------------

        if current_status == "SENT":

            print(
                f"Email job {email_job_id} "
                "already processed"
            )

            channel.basic_ack(
                delivery_tag=method.delivery_tag
            )

            return

        # -----------------------------
        # Mark PROCESSING
        # -----------------------------

        db.execute(
            text(
                """
                UPDATE email_jobs
                SET status = 'PROCESSING'
                WHERE id = :id
                """
            ),
            {
                "id": email_job_id
            },
        )

        db.commit()

        # -----------------------------
        # Send email
        # -----------------------------

        email_service.send_email(
            recipient=recipient,
            subject=subject,
            body=email_body,
        )

        # -----------------------------
        # Mark SENT
        # -----------------------------

        db.execute(
            text(
                """
                UPDATE email_jobs
                SET
                    status = 'SENT',
                    sent_at = :sent_at
                WHERE id = :id
                """
            ),
            {
                "id": email_job_id,
                "sent_at": datetime.now(timezone.utc),
            },
        )

        db.commit()

        # -----------------------------
        # ACK RabbitMQ
        # -----------------------------

        channel.basic_ack(
            delivery_tag=method.delivery_tag
        )

        print(
            f"Email job {email_job_id} "
            "completed successfully"
        )

    except Exception as error:

        print(
            f"Email processing failed: {error}"
        )

        db.rollback()

        # Don't acknowledge the message.
        #
        # RabbitMQ will requeue it.
        channel.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True,
        )

    finally:

        db.close()


def start_worker():

    rabbitmq.connect()

    print(
        "================================"
    )

    print(
        "Email Consumer Started"
    )

    print(
        "Queue: email_queue"
    )

    print(
        "Waiting for messages..."
    )

    print(
        "================================"
    )

    rabbitmq.channel.basic_consume(
        queue="email_queue",
        on_message_callback=process_message,
        auto_ack=False,
    )

    try:

        rabbitmq.channel.start_consuming()

    except KeyboardInterrupt:

        print(
            "Stopping consumer..."
        )

        rabbitmq.close()


if __name__ == "__main__":

    start_worker()