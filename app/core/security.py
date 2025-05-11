from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.core.config import jwt_config
from app.core.exceptions import AuthenticationException
from app.schemas.auth import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, expires_delta: timedelta = timedelta(hours=1)):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, jwt_config.access_secret_key, algorithm=jwt_config.algorithm
    )
    return encoded_jwt, expire


def create_refresh_token(subject: str, expires_delta: timedelta = timedelta(days=7)):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, jwt_config.refresh_secret_key, algorithm=jwt_config.algorithm
    )
    return encoded_jwt


def decode_refresh_token(token: str) -> TokenPayload:
    credentials_exception = AuthenticationException(
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, jwt_config.refresh_secret_key, algorithms=[jwt_config.algorithm]
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenPayload(sub=sub)
        return token_data
    except InvalidTokenError as exc:
        raise credentials_exception from exc


def decode_access_token(token: str) -> TokenPayload:
    credentials_exception = AuthenticationException(
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, jwt_config.access_secret_key, algorithms=[jwt_config.algorithm]
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenPayload(sub=sub, exp=payload.get("exp"))
    except InvalidTokenError as exc:
        raise credentials_exception from exc

    return token_data
