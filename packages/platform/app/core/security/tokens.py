from datetime import datetime, timedelta, timezone

import jwt

from app.api.resources.auth.schemas.dto import TokenPayload
from app.core.config import jwt_config
from app.core.exceptions import AuthenticationException


def create_token(
    subject: str, expires_delta: timedelta, secret_key: str, algorithm: str
):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt, expire


def decode_token(token: str, secret_key: str, algorithm: str) -> TokenPayload:
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    return TokenPayload(sub=payload.get("sub"), exp=payload.get("exp"))


def create_access_token(subject: str, expires_delta: timedelta = timedelta(hours=1)):
    return create_token(
        subject, expires_delta, jwt_config.access_secret_key, jwt_config.algorithm
    )


def create_refresh_token(subject: str, expires_delta: timedelta = timedelta(days=7)):
    return create_token(
        subject, expires_delta, jwt_config.refresh_secret_key, jwt_config.algorithm
    )


def decode_refresh_token(token: str) -> TokenPayload:
    credentials_exception = AuthenticationException(
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return decode_token(token, jwt_config.refresh_secret_key, jwt_config.algorithm)
    except jwt.InvalidTokenError as exc:
        raise credentials_exception from exc


def decode_access_token(token: str) -> TokenPayload:
    credentials_exception = AuthenticationException(
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        return decode_token(token, jwt_config.access_secret_key, jwt_config.algorithm)
    except jwt.InvalidTokenError as exc:
        raise credentials_exception from exc
