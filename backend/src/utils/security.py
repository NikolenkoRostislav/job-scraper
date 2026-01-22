from datetime import datetime, timedelta, timezone
from hashlib import sha256
from passlib.context import CryptContext
from jose import jwt
from src.config import settings


# Password
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def validate_password_complexity(password: str) -> str:
    if not 8 <= len(password) <= 24:
        raise ValueError("Password must be between 8 and 24 characters long")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase character")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase character")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")
    if all(c.isalnum() for c in password):
        raise ValueError("Password must contain at least one special character")
    return password

# JWT Token
def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "type": "access", "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": str(user_id), "type": "refresh", "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

def hash_token(token: str):
    return sha256(token.encode()).hexdigest()
