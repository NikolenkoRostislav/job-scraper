from datetime import datetime, timezone
import secrets
import smtplib
from email.message import EmailMessage
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import SendEmail, Email
from src.config import settings
from src.db import EmailVerificationCode
from src.utils.classes import AppError


EMAIL_VERIFICATION_CODE_CREATION_RETRIES = 5

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
    
    @staticmethod
    async def send_email_code(receiver: Email, db: AsyncSession):
        for i in range(EMAIL_VERIFICATION_CODE_CREATION_RETRIES):
            try:
                code = secrets.randbelow(1_000_000)
                code = int(f"{code:06d}")
                email_code = EmailVerificationCode(
                    email=receiver.receiver,
                    code=code,
                    created_at=datetime.now(timezone.utc)
                )
                db.add(email_code)
                await db.commit()
                break
            except:
                pass
        else:
            raise AppError("couldn't save code")

        email = SendEmail(
            receiver=receiver.receiver,
            subject="Email verification code for IT-JobScraper",
            content=f"Thank you for using IT-JobScraper! Your email verification code is {code}, please do not share it with anyone."
        )

        await EmailService.send_email(email)

        return {"message": "email sent"}
            
