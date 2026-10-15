import json
import time
from datetime import datetime

from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.outbox import OutboxEvent
from ..services.queue_service import QueueService


class OutboxPublisher:

    def __init__(self):

        self.queue_service = QueueService()

    def publish_pending_events(self):

        db: Session = SessionLocal()

        try:

            events = (
                db.query(OutboxEvent)
                .filter(
                    OutboxEvent.status == "PENDING"
                )
                .order_by(
                    OutboxEvent.id
                )
                .limit(10)
                .all()
            )

            for event in events:

                try:

                    message = json.loads(
                        event.payload
                    )

                    print(
                        f"Publishing outbox event "
                        f"{event.id}"
                    )

                    self.queue_service.publish(
                        message
                    )

                    event.status = "PUBLISHED"

                    event.published_at = (
                        datetime.utcnow()
                    )

                    db.commit()

                    print(
                        f"Event {event.id} published"
                    )

                except Exception as error:

                    db.rollback()

                    print(
                        f"Failed to publish "
                        f"event {event.id}: "
                        f"{error}"
                    )

        finally:

            db.close()

    def run(self):

        print(
            "=============================="
        )

        print(
            "Outbox Publisher Started"
        )

        print(
            "=============================="
        )

        while True:

            try:

                self.publish_pending_events()

            except Exception as error:

                print(
                    f"Publisher error: {error}"
                )

            time.sleep(2)


if __name__ == "__main__":

    publisher = OutboxPublisher()

    publisher.run()