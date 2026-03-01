import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from core.config import settings
from pydantic import EmailStr
from shared.models import EmailVerificationCode
from shared.schemas import Email
from shared.services.user import UserService
from shared.utils import AlreadyExistsError, AppError, InvalidEntryError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

CODE_CREATION_RETRIES = 5


class EmailService:
    @staticmethod
    async def send_email(email: Email):
        msg = EmailMessage()
        msg["Subject"] = email.subject
        msg["From"] = settings.email.EMAIL_ADDRESS
        msg["To"] = email.receiver
        msg.set_content(email.content)
        if email.html_content:
            msg.add_alternative(email.html_content, subtype="html")

        with smtplib.SMTP_SSL(
            settings.email.EMAIL_DOMAIN, settings.email.EMAIL_PORT
        ) as smtp:
            smtp.login(settings.email.EMAIL_ADDRESS, settings.email.EMAIL_PASSWORD)
            smtp.send_message(msg)

        return {"message": "Email sent"}

    @staticmethod
    async def create_email_code(db: AsyncSession, email: EmailStr):
        user = await UserService.get_user_by_email(db, email)
        if user:
            raise AlreadyExistsError(
                "Can't create registration code, user with this email already exists"
            )

        result = await db.execute(
            select(EmailVerificationCode).where(EmailVerificationCode.email == email)
        )
        existing_code = result.scalar_one_or_none()

        for i in range(CODE_CREATION_RETRIES):
            try:
                code = secrets.randbelow(900_000) + 100_000
                code = int(f"{code:06d}")

                if existing_code:
                    existing_code.code = code
                    existing_code.created_at = datetime.now(timezone.utc)
                    await db.commit()
                    return existing_code.code
                else:
                    email_code = EmailVerificationCode(
                        email=email, code=code, created_at=datetime.now(timezone.utc)
                    )
                    db.add(email_code)
                    await db.commit()
                    return email_code.code
            except Exception:
                pass
        else:
            raise AppError("couldn't save code")

    @staticmethod
    async def send_email_code(receiver: EmailStr, code: int):
        email = Email(
            receiver=receiver,
            subject="Email verification code for IT-JobScraper",
            content=f"Thank you for using IT-JobScraper! \nYour email verification code is \n{code} \nplease do not share it with anyone.",
            html_content=f"""\
            <html>
              <head></head>
              <body style="font-family: Arial, sans-serif;">
                <h2>Email confirmation</h2>
                <p>Thank you for using IT-JobScraper!</p>
                <p>Your verification code is:</p>
                <div style="font-size: 28px; font-weight: bold; letter-spacing: 4px; margin: 16px 0;">
                  {code}
                </div>
                <p>This code expires in <b>{settings.email.EMAIL_CODE_TTL_MINUTES} minutes</b>.</p>
                <p>Please do <b>not</b> share this code with anyone.</p>
              </body>
            </html>
            """,
        )

        await EmailService.send_email(email)

        return {"message": "email sent"}

    @staticmethod
    async def check_email_code(db: AsyncSession, email: str, code: int) -> bool:
        result = await db.scalars(
            select(EmailVerificationCode).where(EmailVerificationCode.email == email)
        )
        correct_email_code = result.one_or_none()

        if not correct_email_code:
            raise InvalidEntryError("No confirmation code exists for this email")

        if datetime.now(timezone.utc) - correct_email_code.created_at > timedelta(
            minutes=settings.email.EMAIL_CODE_TTL_MINUTES
        ):
            raise InvalidEntryError("The confirmation code is expired")

        if code == correct_email_code.code:
            return True
        return False
