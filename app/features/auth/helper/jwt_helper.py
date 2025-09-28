from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from ....core.app_config import app_config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"token_type": "access", "exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, app_config.SECRET_KEY, algorithm=app_config.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=app_config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"token_type": "refresh", "exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, app_config.SECRET_KEY, algorithm=app_config.ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, app_config.SECRET_KEY, algorithms=[app_config.ALGORITHM])
        if payload["exp"] < datetime.now().timestamp():
            return None
        return payload
    except JWTError:
        return None