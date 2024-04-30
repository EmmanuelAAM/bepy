from core.config import settings
from dependencies.database import get_db
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from models.user_model import User, UserWithRestrictedProperties
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

from schemas.user_schema import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username: str, db: Session, model: UserWithRestrictedProperties | User  = UserWithRestrictedProperties):
    user_db = db.query(model).filter(User.username == username).first()
    return user_db

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)  + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_token(token: str):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payload

def get_current_user(token: str, db: Session):
    payload = decode_token(token)
    username: Optional[str] = payload.get("sub")
    print(username)
    current_user = get_user_by_username(username, db, User)
    return current_user

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Parameters:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the hashed version.

    Parameters:
        plain_password (str): The plain text password.
        hashed_password (str): The bcrypt hashed password from your database.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


