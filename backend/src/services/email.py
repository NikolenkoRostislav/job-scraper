import secrets
import smtplib
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings
from src.db import EmailVerificationCode
from src.schemas import SendEmail, Email
from src.services.user import UserService
from src.utils.classes import AppError, PermissionDeniedError, InvalidEntryError


CODE_CREATION_RETRIES = 5
CODE_EXPIRES_IN = timedelta(minutes=settings.EMAIL_CODE_TTL_MINUTES)

class EmailService:
    @staticmethod
    async def send_email(email: SendEmail):
        msg = EmailMessage()
        msg['Subject'] = email.subject
        msg['From'] = settings.EMAIL_ADDRESS
        msg['To'] = email.receiver
        msg.set_content(email.content)
        if email.html_content:
            msg.add_alternative(email.html_content, subtype="html")

        with smtplib.SMTP_SSL(settings.EMAIL_DOMAIN, settings.EMAIL_PORT) as smtp:
            smtp.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            smtp.send_message(msg)

        return {"message": "Email sent"}
    
    @staticmethod
    async def send_email_code(receiver: Email, db: AsyncSession):
        user = await UserService.get_user_by_email(receiver.receiver, db)
        if user:
            raise PermissionDeniedError("Can't create registration code, user with this email already exists")

        result = await db.execute(
            select(EmailVerificationCode).where(EmailVerificationCode.email == receiver.receiver)
        )
        existing_code = result.scalar_one_or_none()

        for i in range(CODE_CREATION_RETRIES):
            try:
                code = secrets.randbelow(900_000) + 100_000
                code = int(f"{code:06d}")

                if existing_code:
                    existing_code.code = code
                    existing_code.created_at = datetime.now(timezone.utc)
                else:
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
                <p>This code expires in <b>15 minutes</b>.</p>
                <p>Please do <b>not</b> share this code with anyone.</p>
              </body>
            </html>
            """
        )

        await EmailService.send_email(email)

        return {"message": "email sent"}
    
        
    @staticmethod
    async def check_email_code(email: str, code: int, db: AsyncSession) -> bool:
        result = await db.scalars(select(EmailVerificationCode).where(EmailVerificationCode.email == email))   
        correct_email_code = result.one_or_none()
        if not correct_email_code or datetime.now(timezone.utc) - correct_email_code.created_at > CODE_EXPIRES_IN:
            raise InvalidEntryError("No confirmation code exists for this email or the code is expired")
        
        if code == correct_email_code.code:
            return True
        return False
