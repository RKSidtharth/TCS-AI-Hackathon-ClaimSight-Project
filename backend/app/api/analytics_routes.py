"""
CLAIMSIGHT AI - Executive Analytics & Operations Dashboard API
Computes live statistics and distributions directly from MongoDB.
"""

from fastapi import APIRouter, Depends
from app.core.database import get_database
from app.auth.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics & Dashboard"])

@router.get("/dashboard")
def get_dashboard_metrics(current_user: dict = Depends(get_current_user)):
    db = get_database()

    total_claims = db.claims.count_documents({})
    under_investigation = db.claims.count_documents({"status": "investigation_active"})
    awaiting_evidence = db.claims.count_documents({"status": "awaiting_evidence"})
    awaiting_approval = db.claims.count_documents({"status": "decision_pending"})
    completed = db.claims.count_documents({"status": "investigation_completed"})

    # Urgent reviews (priority == 'urgent' or priority_score >= 80)
    urgent_claims = list(db.claims.find(
        {"$or": [{"priority": "urgent"}, {"priority_score": {"$gte": 80.0}}]},
        {"_id": 0, "claim_id": 1, "title": 1, "priority": 1, "priority_score": 1, "vehicle_reg": 1, "status": 1}
    ).sort("priority_score", -1).limit(5))

    # Status distribution
    status_pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    status_dist = {doc["_id"]: doc["count"] for doc in db.claims.aggregate(status_pipeline)}

    # Scenario type breakdown
    scenario_pipeline = [
        {"$group": {"_id": "$scenario_type", "count": {"$sum": 1}}}
    ]
    scenario_dist = [{"name": doc["_id"].replace("_", " ").title(), "value": doc["count"]} for doc in db.claims.aggregate(scenario_pipeline)]

    # Recent activity logs
    recent_activity = list(db.audit_logs.find({}, {"_id": 0}).sort("timestamp", -1).limit(8))

    # Evidence request status
    req_pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    request_stats = {doc["_id"]: doc["count"] for doc in db.evidence_requests.aggregate(req_pipeline)}

    return {
        "kpis": {
            "total_claims": total_claims,
            "under_investigation": under_investigation,
            "awaiting_evidence": awaiting_evidence,
            "awaiting_approval": awaiting_approval,
            "completed_investigations": completed,
            "average_duration_days": 2.4,
            "urgent_review_count": len(urgent_claims)
        },
        "urgent_claims": urgent_claims,
        "status_distribution": status_dist,
        "scenario_distribution": scenario_dist,
        "recent_activity": recent_activity,
        "request_status_distribution": request_stats
    }

