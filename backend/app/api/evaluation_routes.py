"""
CLAIMSIGHT AI - Claim Evaluation & Counterfactual Sandbox Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_database
from app.auth.security import get_current_user
from app.ai.claim_evaluation.plausibility_evaluator import PlausibilityEvaluator
from app.ai.incident_reconstruction.hypothesis_engine import IncidentReconstructionEngine
from app.schemas.evaluation import CounterfactualRequest, CounterfactualResponse

router = APIRouter(tags=["Claim Evaluation"])

@router.get("/claims/{claim_id}/evaluation")
def get_claim_evaluation(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    eval_doc = db.claim_evaluations.find_one({"claim_id": claim_id}, {"_id": 0})
    if not eval_doc:
        claim = db.claims.find_one({"claim_id": claim_id})
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        evidence = list(db.evidence.find({"claim_id": claim_id}))
        eval_doc = PlausibilityEvaluator.evaluate_claim(claim, evidence)
        db.claim_evaluations.insert_one(eval_doc)
        eval_doc.pop("_id", None)

    return eval_doc

@router.post("/claims/{claim_id}/evaluate")
def recompute_evaluation(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    evidence = list(db.evidence.find({"claim_id": claim_id}))
    eval_doc = PlausibilityEvaluator.evaluate_claim(claim, evidence)

    db.claim_evaluations.update_one(
        {"claim_id": claim_id},
        {"$set": eval_doc},
        upsert=True
    )

    return {"message": "Claim evaluation recomputed successfully", "evaluation": eval_doc}

@router.post("/claims/{claim_id}/counterfactual", response_model=CounterfactualResponse)
def run_counterfactual_simulation(
    claim_id: str,
    payload: CounterfactualRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Simulates counterfactual what-if conditions without modifying original claim evidence.
    """
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id}, {"_id": 0})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    hypotheses = list(db.accident_hypotheses.find({"claim_id": claim_id}, {"_id": 0}))
    current_estimate = float(claim.get("estimated_damage", 0))

    sim_result = IncidentReconstructionEngine.run_counterfactual_simulation(
        claim_data=claim,
        assumption=payload.assumption,
        current_hypotheses=hypotheses,
        current_estimate=current_estimate
    )

    # Persist in counterfactual_scenarios collection for session history
    db.counterfactual_scenarios.insert_one({
        "scenario_id": sim_result["scenario_id"],
        "claim_id": claim_id,
        "assumption": payload.assumption,
        "result": sim_result,
        "created_by": current_user["user_id"]
    })

    return {
        "scenario_id": sim_result["scenario_id"],
        "assumption": payload.assumption,
        "affected_relationships": sim_result["affected_relationships"],
        "recalculated_hypotheses": hypotheses,
        "settlement_difference": sim_result["settlement_difference"],
        "new_indicative_payout": sim_result["new_indicative_payout"],
        "explanation": sim_result["explanation"]
    }

@router.get("/claims/{claim_id}/benchmarks")
def get_repair_benchmarks(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    vehicle = db.vehicles.find_one({"claim_id": claim_id}, {"_id": 0})
    if not vehicle:
        return {"benchmarks": []}

    benchmarks = list(db.repair_benchmarks.find({
        "make": vehicle.get("make"),
        "model": {"$regex": vehicle.get("model", "").split()[0], "$options": "i"}
    }, {"_id": 0}))

    if not benchmarks:
        benchmarks = list(db.repair_benchmarks.find({}, {"_id": 0}).limit(5))

    return {"claim_id": claim_id, "vehicle": vehicle, "benchmarks": benchmarks}

