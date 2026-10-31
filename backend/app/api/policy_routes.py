"""
CLAIMSIGHT AI - Policy & Settlement Intelligence API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_database
from app.auth.security import get_current_user
from app.ai.policy_engine.coverage_rules import PolicyEngine

router = APIRouter(tags=["Policy & Settlement"])

@router.get("/claims/{claim_id}/coverage")
def get_claim_coverage(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    policy_number = claim.get("policy_number")
    policy = db.policies.find_one({"policy_number": policy_number}, {"_id": 0})
    versions = list(db.policy_versions.find({"policy_number": policy_number}, {"_id": 0}).sort("version_number", 1))

    inc_date = f"{claim.get('incident_date')}T{claim.get('incident_time')}Z"
    applicable_version = PolicyEngine.get_applicable_policy_version(policy_number, inc_date)
    applicable_version.pop("_id", None) if "_id" in applicable_version else None

    return {
        "claim_id": claim_id,
        "policy": policy,
        "incident_datetime": inc_date,
        "applicable_version": applicable_version,
        "version_history": versions,
        "is_transition_period": len(versions) > 1
    }

@router.get("/claims/{claim_id}/settlement-recommendation")
def get_settlement_recommendation(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id}, {"_id": 0})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    policy = db.policies.find_one({"policy_number": claim.get("policy_number")}, {"_id": 0}) or {}
    estimate_amount = float(claim.get("estimated_damage", 0))

    settlement = PolicyEngine.calculate_settlement(claim, estimate_amount, policy)
    return settlement

