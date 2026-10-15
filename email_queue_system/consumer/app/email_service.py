import smtplib
from email.message import EmailMessage

from .config import settings


class EmailService:

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
    ):

        message = EmailMessage()

        message["From"] = settings.EMAIL_FROM
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
        ) as smtp:

            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )

            smtp.send_message(message)

        print(
            f"Email successfully sent to {recipient}"
        )