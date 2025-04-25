# ============================================================
# app/api/routes/auth.py
# ============================================================
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# Mock credential store
CLIENTS = {
    "ORG_123": {"secret": "org_secret", "scope": "org.verify"},
    "USER_456": {"secret": "user_secret", "scope": "user.submit"},
    "ADMIN_789": {"secret": "admin_secret", "scope": "admin.review"},
}

class TokenRequest(BaseModel):
    client_id: str
    client_secret: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/token", response_model=TokenResponse)
async def token(req: TokenRequest):
    record = CLIENTS.get(req.client_id)
    if not record or record["secret"] != req.client_secret:
        raise HTTPException(400, "invalid_client")
    token = create_access_token(req.client_id, record["scope"])
    return {"access_token": token}