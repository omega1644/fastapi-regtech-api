# ============================================================
# app/api/routes/admin.py
# ============================================================
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId

from app.api.deps import require_scope
from app.domain.schemas import AdminPatch
from app.infrastructure.mongo.models import VerificationDoc

router = APIRouter(prefix="/admin/verifications", tags=["admin"])

@router.patch("/{ver_id}", dependencies=[Depends(require_scope("admin.review"))])
async def patch_verification(ver_id: UUID, body: AdminPatch):
    doc = await VerificationDoc.get(PydanticObjectId(ver_id))
    if not doc:
        raise HTTPException(404, "Not Found")
    doc.status = body.status
    doc.outcome = body.outcome
    doc.reason = body.reason
    await doc.save()
    return {"success": True}
