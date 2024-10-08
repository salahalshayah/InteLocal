import binascii
import hashlib
import logging
import os

from app.db.crud import get_user_by_id
from app.db.database import get_db
from config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY


async def hash_password(password: str) -> str:
    """Hash a password with a unique salt using SHA-256."""
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    salt_hex = binascii.hexlify(salt).decode('utf-8')
    hash_hex = binascii.hexlify(hashed_password).decode('utf-8')
    return f"{salt_hex}${hash_hex}"


async def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a provided password against the stored hashed password."""
    salt_hex, stored_hash = stored_password.split('$')
    salt = binascii.unhexlify(salt_hex)
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    new_hash_hex = binascii.hexlify(new_hash).decode('utf-8')
    return new_hash_hex == stored_hash


def create_access_token(data: dict):
    """Generate a JWT token with the provided data."""
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("*-/*-/*-/payload", payload)
        user_id = payload.get("user_id")  # or "sub" if applicable
        if user_id is None:
            print("he")
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user = await get_user_by_id(user_id, db)
    if user is None:
        raise credentials_exception
    return user
