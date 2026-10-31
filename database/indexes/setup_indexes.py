"""
CLAIMSIGHT AI - Database Index Setup
Initializes optimized compound and unique indexes for all 22 collections.
"""

import os
import pymongo
from pymongo import ASCENDING, DESCENDING

def create_all_indexes(uri: str = None, db_name: str = "claimsight_ai"):
    if not uri:
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    print(f"[*] Setting up indexes on MongoDB database: '{db_name}'...")

    # 1. users
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.users.create_index([("role", ASCENDING)])

    # 2. claims
    db.claims.create_index([("claim_id", ASCENDING)], unique=True)
    db.claims.create_index([("status", ASCENDING), ("created_at", DESCENDING)])
    db.claims.create_index([("policy_number", ASCENDING)])
    db.claims.create_index([("vehicle_reg", ASCENDING)])
    db.claims.create_index([("priority_score", DESCENDING)])

    # 3. vehicles
    db.vehicles.create_index([("vehicle_id", ASCENDING)], unique=True)
    db.vehicles.create_index([("registration_number", ASCENDING)])
    db.vehicles.create_index([("vin", ASCENDING)])

    # 4. policies
    db.policies.create_index([("policy_id", ASCENDING)], unique=True)
    db.policies.create_index([("policy_number", ASCENDING)], unique=True)

    # 5. policy_versions
    db.policy_versions.create_index([("version_id", ASCENDING)], unique=True)
    db.policy_versions.create_index([("policy_number", ASCENDING), ("effective_from", ASCENDING)])

    # 6. evidence
    db.evidence.create_index([("evidence_id", ASCENDING)], unique=True)
    db.evidence.create_index([("claim_id", ASCENDING), ("created_at", ASCENDING)])
    db.evidence.create_index([("sha256_hash", ASCENDING)])

    # 7. extracted_facts
    db.extracted_facts.create_index([("fact_id", ASCENDING)], unique=True)
    db.extracted_facts.create_index([("claim_id", ASCENDING), ("evidence_id", ASCENDING)])
    db.extracted_facts.create_index([("category", ASCENDING)])

    # 8. evidence_relationships
    db.evidence_relationships.create_index([("relationship_id", ASCENDING)], unique=True)
    db.evidence_relationships.create_index([("claim_id", ASCENDING)])
    db.evidence_relationships.create_index([("source_id", ASCENDING), ("target_id", ASCENDING)])

    # 9. witness_statements
    db.witness_statements.create_index([("statement_id", ASCENDING)], unique=True)
    db.witness_statements.create_index([("claim_id", ASCENDING)])

    # 10. investigation_timelines
    db.investigation_timelines.create_index([("timeline_id", ASCENDING)], unique=True)
    db.investigation_timelines.create_index([("claim_id", ASCENDING), ("event_timestamp", ASCENDING)])

    # 11. accident_hypotheses
    db.accident_hypotheses.create_index([("hypothesis_id", ASCENDING)], unique=True)
    db.accident_hypotheses.create_index([("claim_id", ASCENDING)])

    # 12. claim_evaluations
    db.claim_evaluations.create_index([("evaluation_id", ASCENDING)], unique=True)
    db.claim_evaluations.create_index([("claim_id", ASCENDING)])

    # 13. repair_estimates
    db.repair_estimates.create_index([("estimate_id", ASCENDING)], unique=True)
    db.repair_estimates.create_index([("claim_id", ASCENDING)])

    # 14. repair_benchmarks
    db.repair_benchmarks.create_index([("benchmark_id", ASCENDING)], unique=True)
    db.repair_benchmarks.create_index([("make", ASCENDING), ("model", ASCENDING), ("component", ASCENDING)])

    # 15. evidence_requests
    db.evidence_requests.create_index([("request_id", ASCENDING)], unique=True)
    db.evidence_requests.create_index([("claim_id", ASCENDING), ("status", ASCENDING)])
    db.evidence_requests.create_index([("rank_score", DESCENDING)])

    # 16. investigation_reports
    db.investigation_reports.create_index([("report_id", ASCENDING)], unique=True)
    db.investigation_reports.create_index([("claim_id", ASCENDING)])

    # 17. investigator_decisions
    db.investigator_decisions.create_index([("decision_id", ASCENDING)], unique=True)
    db.investigator_decisions.create_index([("claim_id", ASCENDING)])

    # 18. audit_logs
    db.audit_logs.create_index([("log_id", ASCENDING)], unique=True)
    db.audit_logs.create_index([("claim_id", ASCENDING), ("timestamp", DESCENDING)])
    db.audit_logs.create_index([("user_id", ASCENDING)])

    # 19. notifications
    db.notifications.create_index([("notification_id", ASCENDING)], unique=True)
    db.notifications.create_index([("user_id", ASCENDING), ("read", ASCENDING)])
    db.notifications.create_index([("claim_id", ASCENDING)])

    # 20. model_registry
    db.model_registry.create_index([("model_id", ASCENDING)], unique=True)
    db.model_registry.create_index([("model_name", ASCENDING), ("version", ASCENDING)])

    # 21. external_data_records
    db.external_data_records.create_index([("record_id", ASCENDING)], unique=True)
    db.external_data_records.create_index([("claim_id", ASCENDING), ("source", ASCENDING)])

    # 22. counterfactual_scenarios
    db.counterfactual_scenarios.create_index([("scenario_id", ASCENDING)], unique=True)
    db.counterfactual_scenarios.create_index([("claim_id", ASCENDING)])

    print("[OK] All 22 collection indexes established successfully.")

if __name__ == "__main__":
    create_all_indexes()
