# ============================================================
# app/api/deps.py
# ============================================================
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.infrastructure.mongo.connection import init_mongo

_token_scheme = HTTPBearer(auto_error=False)

ROLE_SCOPE = {
    "org": "org.verify",
    "user": "user.submit",
    "admin": "admin.review",
}

async def startup_mongo():
    await init_mongo()

async def get_current_token(credentials: HTTPAuthorizationCredentials = Security(_token_scheme)):
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing auth header")
    return decode_token(credentials.credentials)


def require_scope(scope: str):
    async def _checker(token=Depends(get_current_token)):
        if token.get("scope") != scope:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid scope")
        return token
    return _checker