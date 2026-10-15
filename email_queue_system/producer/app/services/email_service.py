from ..config import settings


class EmailService:

    @staticmethod
    def create_welcome_email(
        name: str,
        email: str,
    ) -> dict:

        return {
            "recipient": email,
            "subject": "Welcome to our application",
            "body": f"""Hello {name},

Welcome to our application!

Your account has been successfully created.

Thank you,
Email Queue System
""",
        }