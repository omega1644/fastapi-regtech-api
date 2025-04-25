# ============================================================
# app/domain/schemas.py  (HTTP contract)
# ============================================================
from datetime import date
from uuid import UUID
from pydantic import BaseModel
from app.infrastructure.mongo.models import VerificationStatus, Employee


class VerificationCreate(BaseModel):
    employee: Employee


class VerificationRead(BaseModel):
    id: UUID
    status: VerificationStatus
    outcome: str | None = None
    reason: str | None = None


class AdminPatch(BaseModel):
    status: VerificationStatus
    outcome: str | None = None
    reason: str | None = None