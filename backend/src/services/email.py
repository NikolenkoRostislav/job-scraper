import smtplib
from email.message import EmailMessage
from src.schemas import SendEmail
from src.config import settings


class EmailService:
    @staticmethod
    async def send_email(email: SendEmail):
        msg = EmailMessage()
        msg['Subject'] = email.subject
        msg['From'] = settings.EMAIL_ADDRESS
        msg['To'] = email.receiver
        msg.set_content(email.content)

        with smtplib.SMTP_SSL(settings.EMAIL_DOMAIN, settings.EMAIL_PORT) as smtp:
            smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            smtp.send_message(msg)

        return {"message": "Email sent"}
