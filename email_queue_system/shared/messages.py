from dataclasses import dataclass


@dataclass
class EmailMessage:

    event_type: str

    email_job_id: int

    recipient: str

    subject: str

    body: str

    retry_count: int = 0