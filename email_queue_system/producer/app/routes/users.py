import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.email_job import EmailJob
from ..models.outbox import OutboxEvent

from ..schemas.user import UserCreate
from ..schemas.user import UserResponse

from ..services.email_service import EmailService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=201,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    email = str(user_data.email)

    # --------------------------------
    # Check duplicate user
    # --------------------------------

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    # --------------------------------
    # Create user
    # --------------------------------

    user = User(
        name=user_data.name,
        email=email,
    )

    db.add(user)

    # Flush gives us the generated ID
    # without committing the transaction.

    db.flush()

    # --------------------------------
    # Create email
    # --------------------------------

    email_data = EmailService.create_welcome_email(
        name=user.name,
        email=user.email,
    )

    email_job = EmailJob(
        user_id=user.id,
        recipient=email_data["recipient"],
        subject=email_data["subject"],
        body=email_data["body"],
        status="PENDING",
    )

    db.add(email_job)

    db.flush()

    # --------------------------------
    # Create outbox event
    # --------------------------------

    message = {
        "event_type": "WELCOME_EMAIL",
        "email_job_id": email_job.id,
        "recipient": email_job.recipient,
        "subject": email_job.subject,
        "body": email_job.body,
        "retry_count": 0,
    }

    outbox_event = OutboxEvent(
        event_type="WELCOME_EMAIL",
        payload=json.dumps(message),
        status="PENDING",
    )

    db.add(outbox_event)

    # --------------------------------
    # ONE transaction
    # --------------------------------

    db.commit()

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        status="EMAIL_QUEUED",
    )