"""
CLAIMSIGHT AI - Police File & Priority Reference #1 Synthetic Data Enrichment Script
Populates every claim in the database with:
1. Official Police General Diary / FIR Extract particulars.
2. Ingested Police File document in evidence.
3. Priority Reference #1: Consumer File vs. Police Report Mismatch contradiction.
4. Next-Best-Evidence intelligence recommendations.
"""

import datetime
from pymongo import MongoClient

def enrich_data():
    client = MongoClient("mongodb://localhost:27017")
    db = client["claimsight_ai"]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    claims = list(db.claims.find({}))
    print(f"[*] Processing {len(claims)} claims...")

    for c in claims:
        cid = c["claim_id"]
        pol_no = c.get("policy_number", "POL-DEFAULT")
        narrative = c.get("reported_narrative", "Driver states collision occurred without secondary impact.")
        station = "Indiranagar Traffic Police Station" if "002" in cid or "001" in cid else "Koramangala Traffic Police Station"
        gd_no = f"GD-{cid[-3:]}/2026"
        police_summary = (
            f"Station General Diary extract records two-vehicle dynamic impact with road skid vectors and conflicting damage locus; "
            f"contradicts driver intake declaration asserting single-point collision while stationary."
        )

        # 1. Update claim police report field
        db.claims.update_one(
            {"claim_id": cid},
            {"$set": {
                "police_report": {
                    "station_name": station,
                    "fir_gd_number": gd_no,
                    "officer_name": "Sub-Inspector R. Ramesh",
                    "police_summary": police_summary,
                    "has_discrepancy": True
                }
            }}
        )

        # 2. Ingest Police Report Evidence item
        pol_ev_id = f"EVD-{cid}-POLICE"
        if not db.evidence.find_one({"claim_id": cid, "evidence_id": pol_ev_id}):
            db.evidence.insert_one({
                "evidence_id": pol_ev_id,
                "claim_id": cid,
                "file_name": f"official_police_gd_{gd_no.replace('/', '_')}.pdf",
                "file_type": "document",
                "source": f"Official Police Station ({station})",
                "file_size": "1.8 MB",
                "sha256_hash": "7d8a9b0c1e2f3456789abcdef0123456789abcdef0123456789abcdef01234567",
                "notes": [
                    f"Official Station GD Extract #{gd_no}",
                    "Attending Officer: Sub-Inspector R. Ramesh",
                    police_summary
                ],
                "created_at": now
            })

        # 3. Upsert Priority Reference #1 Contradiction
        first_rel_id = f"REL-{cid}-PRIORITY-1"
        first_ref_desc = (
            f"PRIORITY REFERENCE #1: Consumer file narrative claims '{narrative[:85]}...', "
            f"whereas Official Police General Diary ({gd_no} - {station}) records dynamic moving collision "
            f"with conflicting damage locus and driver divergence at scene."
        )
        db.evidence_relationships.update_one(
            {"relationship_id": first_rel_id},
            {"$set": {
                "relationship_id": first_rel_id,
                "claim_id": cid,
                "relationship_type": "Contradicts",
                "source_id": "Consumer File (Claimant Statement)",
                "target_id": "Official Police File (GD / FIR Extract)",
                "severity": "Critical (Priority Reference #1)",
                "explanation": first_ref_desc,
                "materiality": "Fundamental (Primary Reference) - Direct factual mismatch between consumer sworn declaration and official police station record.",
                "alternative_explanations": [
                    "Policyholder experienced trauma or disorientation during intake statement",
                    "Police GD records preliminary dispatch observation rather than exact crash instant",
                    "Deliberate omission of crash mechanics to avoid contributory fault deduction"
                ],
                "resolution_evidence": f"Request certified Station GD folio from {station} and examine attending officer.",
                "confidence": 0.94,
                "created_at": now
            }},
            upsert=True
        )

        # 4. Ingest NBE recommendations if none exist
        if db.evidence_requests.count_documents({"claim_id": cid}) == 0:
            db.evidence_requests.insert_one({
                "request_id": f"REC-{cid}-1",
                "claim_id": cid,
                "action": f"Request Certified General Diary Folio from {station}",
                "priority": "High",
                "uncertainty_addressed": "Resolves Priority Reference #1 discrepancy between consumer statement and police crash log.",
                "expected_information_gain": 0.88,
                "materiality": 0.92,
                "reliability": 0.96,
                "estimated_cost": 0.05,
                "rank_score": 1.88,
                "status": "pending",
                "responsible_party": "Investigator",
                "created_at": now
            })

    print("[OK] Successfully enriched all claims with Police Reports, Priority Reference #1 Contradictions, and NBE recommendations.")

if __name__ == "__main__":
    enrich_data()

