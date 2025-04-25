# ============================================================
# app/api/routes/verifications.py
# ============================================================
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from app.api.deps import require_scope
from app.domain.schemas import VerificationCreate, VerificationRead
from app.infrastructure.mongo.models import VerificationDoc

router = APIRouter(prefix="/verifications", tags=["verifications"])


@router.post("/", response_model=VerificationRead, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_scope("org.verify"))])
async def create_verification(payload: VerificationCreate):
    doc = VerificationDoc(employee=payload.employee)
    await doc.insert()
    return VerificationRead(id=doc.id, status=doc.status)


@router.get("/{ver_id}", response_model=VerificationRead,
            dependencies=[Depends(require_scope("org.verify"))])
async def get_verification(ver_id: UUID):
    doc = await VerificationDoc.get(PydanticObjectId(ver_id))
    if not doc:
        raise HTTPException(404, "Not Found")
    return VerificationRead(id=doc.id, status=doc.status, outcome=doc.outcome, reason=doc.reason)
