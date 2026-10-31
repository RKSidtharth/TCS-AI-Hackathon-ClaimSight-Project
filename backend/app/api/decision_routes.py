"""
CLAIMSIGHT AI - Investigator Decisions & SIU Audit Endpoints
"""

import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_database
from app.core.config import settings
from app.auth.security import get_current_user
from app.schemas.reports import DecisionCreate, NoteCreate
from app.services.audit_service import AuditService

router = APIRouter(tags=["Investigator Decisions"])

@router.post("/claims/{claim_id}/decisions")
def record_decision(
    claim_id: str,
    payload: DecisionCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim_amount = float(payload.approved_settlement_amount or claim.get("estimated_damage", 0))
    is_high_impact = claim_amount >= settings.HIGH_IMPACT_THRESHOLD_INR

    # STRICT GUARDRAIL ENFORCEMENT:
    # AI should support, not autonomously make, high-impact insurance decisions.
    # Claims over ₹5 Lakhs MUST be verified by the top insurance executive (Admin role).
    if payload.status == "approved" and is_high_impact:
        if current_user.get("role") != "admin":
            AuditService.log(
                claim_id,
                current_user["user_id"],
                "GUARDRAIL_INTERCEPTION",
                f"Blocked non-executive attempt to approve high-impact claim of INR {claim_amount:,.2f} exceeding ₹5L threshold."
            )
            raise HTTPException(
                status_code=403,
                detail=(
                    f"GUARDRAIL ENFORCED: High-Impact Decision Threshold Exceeded (INR {claim_amount:,.2f} >= ₹5,00,000). "
                    "Claims exceeding ₹5 Lakhs cannot be approved by standard investigators or AI models. "
                    "Verification and authorization by the Chief Compliance Officer / Top Insurance Executive is mandatory. "
                    "Please select 'escalated' to forward this dossier to Executive SIU."
                )
            )

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    decision_doc = {
        "decision_id": f"DEC-{claim_id}",
        "claim_id": claim_id,
        "investigator_id": current_user["user_id"],
        "investigator_name": current_user.get("name", "Investigator"),
        "role_at_decision": current_user.get("role"),
        "is_high_impact": is_high_impact,
        "verified_by_top_insurance_officer": current_user.get("role") == "admin" if is_high_impact else True,
        "status": payload.status,
        "notes": payload.notes,
        "approved_settlement_amount": payload.approved_settlement_amount,
        "confirmed_contradictions": payload.confirmed_contradictions or [],
        "dismissed_contradictions": payload.dismissed_contradictions or [],
        "decided_at": now
    }

    db.investigator_decisions.update_one(
        {"claim_id": claim_id},
        {"$set": decision_doc},
        upsert=True
    )

    # Update claim status
    status_map = {
        "approved": "investigation_completed",
        "rejected": "claim_rejected",
        "escalated": "escalated_to_siu",
        "info_requested": "awaiting_evidence"
    }
    new_status = status_map.get(payload.status, "investigation_active")
    db.claims.update_one({"claim_id": claim_id}, {"$set": {"status": new_status, "updated_at": now}})

    AuditService.log(
        claim_id,
        current_user["user_id"],
        "INVESTIGATOR_DECISION_SUBMITTED",
        f"Decision: {payload.status}. Notes: {payload.notes[:80]}..."
    )

    decision_doc.pop("_id", None)
    return {"message": "Investigator decision recorded successfully", "decision": decision_doc}

@router.post("/claims/{claim_id}/notes")
def add_note(
    claim_id: str,
    payload: NoteCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    db.claims.update_one(
        {"claim_id": claim_id},
        {"$push": {"investigator_notes": {
            "author": current_user.get("name", "Investigator"),
            "user_id": current_user["user_id"],
            "note": payload.note,
            "timestamp": now
        }}}
    )

    AuditService.log(claim_id, current_user["user_id"], "NOTE_ADDED", payload.note[:60])
    return {"message": "Note added successfully"}

@router.get("/claims/{claim_id}/audit")
def get_claim_audit_trail(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    logs = list(db.audit_logs.find({"claim_id": claim_id}, {"_id": 0}).sort("timestamp", -1))
    return {"claim_id": claim_id, "total_events": len(logs), "audit_trail": logs}

