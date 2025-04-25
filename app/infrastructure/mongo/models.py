# ============================================================
# app/infrastructure/mongo/models.py
# ============================================================
from datetime import datetime, date
from enum import Enum
from uuid import uuid4, UUID
from beanie import Document
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    PENDING_ORG = "PENDING_ORG"
    PENDING_ADMIN = "PENDING_ADMIN"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Employee(BaseModel):
    first_name: str
    last_name: str
    dob: date


class VerificationDoc(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    employee: Employee
    status: VerificationStatus = VerificationStatus.PENDING_ORG
    outcome: str | None = None
    reason: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "verifications"