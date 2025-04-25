# ============================================================
# app/core/security.py
# ============================================================
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt
from fastapi import HTTPException, status

from .config import get_settings

settings = get_settings()


def create_access_token(subject: str, scope: str) -> str:
    expire = datetime.now() + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode: Dict[str, Any] = {"sub": subject, "scope": scope, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token invalid or expired")