"""
CLAIMSIGHT AI - Next-Best-Evidence Recommendation & Request Endpoints
"""

import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_database
from app.auth.security import get_current_user
from app.schemas.next_best_evidence import EvidenceRequestCreate, EvidenceRequestUpdate
from app.ai.next_best_evidence.recommendation_ranker import NextBestEvidenceRanker
from app.services.audit_service import AuditService

router = APIRouter(tags=["Next-Best-Evidence"])

@router.get("/claims/{claim_id}/evidence-recommendations")
def get_recommendations(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    recs = list(db.evidence_requests.find({"claim_id": claim_id}, {"_id": 0}).sort("rank_score", -1))
    if not recs:
        claim = db.claims.find_one({"claim_id": claim_id})
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        contradictions = list(db.evidence_relationships.find({"claim_id": claim_id}))
        hypotheses = list(db.accident_hypotheses.find({"claim_id": claim_id}))
        eval_doc = db.claim_evaluations.find_one({"claim_id": claim_id}) or {}
        recs = NextBestEvidenceRanker.generate_recommendations(claim, contradictions, hypotheses, eval_doc)
        for r in recs:
            db.evidence_requests.insert_one(r)
            r.pop("_id", None)

    return {
        "claim_id": claim_id,
        "total_recommendations": len(recs),
        "ranking_formula": "Score = (Expected Information Gain × Materiality × Reliability) / (Cost + 0.1)",
        "recommendations": recs
    }

@router.post("/claims/{claim_id}/evidence-requests")
def create_evidence_request(
    claim_id: str,
    payload: EvidenceRequestCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    req_id = f"REQ-{claim_id}-{int(datetime.datetime.now().timestamp() * 1000)}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    new_request = {
        "request_id": req_id,
        "claim_id": claim_id,
        "action_recommended": payload.action_recommended,
        "priority": payload.priority or "High",
        "uncertainty_addressed": payload.uncertainty_addressed,
        "expected_information_gain": 0.85,
        "materiality": 0.80,
        "reliability": 0.95,
        "estimated_cost": 0.15,
        "rank_score": round((0.85 * 0.80 * 0.95) / (0.15 + 0.1), 2),
        "status": "sent",
        "responsible_party": payload.responsible_party or "Claimant",
        "notes": payload.notes,
        "created_at": now
    }
    db.evidence_requests.insert_one(new_request)

    # Insert notification for claimant
    db.notifications.insert_one({
        "notification_id": f"NOTIF-{req_id}",
        "user_id": claim.get("claimant", {}).get("email"),
        "claim_id": claim_id,
        "message": f"Action Required: {payload.action_recommended}",
        "read": False,
        "created_at": now
    })

    AuditService.log(
        claim_id,
        current_user["user_id"],
        "EVIDENCE_REQUEST_ISSUED",
        f"Issued request: {payload.action_recommended} to {payload.responsible_party}"
    )

    new_request.pop("_id", None)
    return {"message": "Evidence request dispatched successfully", "request": new_request}

@router.patch("/evidence-requests/{request_id}")
def update_evidence_request(
    request_id: str,
    payload: EvidenceRequestUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    res = db.evidence_requests.update_one(
        {"request_id": request_id},
        {"$set": {"status": payload.status, "notes": payload.notes}}
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Evidence request not found")

    return {"message": f"Evidence request {request_id} updated to '{payload.status}'"}

