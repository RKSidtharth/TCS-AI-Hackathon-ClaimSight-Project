"""
CLAIMSIGHT AI - Claims Management API Endpoints
"""

import datetime
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.core.database import get_database
from app.auth.security import get_current_user, require_roles
from app.schemas.claims import ClaimCreate, ClaimUpdate, ClaimListResponse
from app.services.audit_service import AuditService

router = APIRouter(prefix="/claims", tags=["Claims"])

@router.get("", response_model=ClaimListResponse)
def list_claims(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: str = Query(None, alias="status"),
    priority_filter: str = Query(None, alias="priority"),
    search: str = Query(None),
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    query = {}

    # Role-based filtering: Claimant only sees their own claims
    if current_user.get("role") == "claimant":
        query["claimant.email"] = current_user.get("email")

    if status_filter:
        query["status"] = status_filter
    if priority_filter:
        query["priority"] = priority_filter
    if search:
        query["$or"] = [
            {"claim_id": {"$regex": search, "$options": "i"}},
            {"title": {"$regex": search, "$options": "i"}},
            {"vehicle_reg": {"$regex": search, "$options": "i"}},
            {"claimant.name": {"$regex": search, "$options": "i"}}
        ]

    total = db.claims.count_documents(query)
    skip = (page - 1) * limit
    cursor = db.claims.find(query, {"_id": 0}).sort("priority_score", -1).skip(skip).limit(limit)
    claims = list(cursor)

    return {"total": total, "page": page, "limit": limit, "claims": claims}

@router.post("", status_code=status.HTTP_201_CREATED)
def create_claim(payload: ClaimCreate, current_user: dict = Depends(get_current_user)):
    # Role check: Senior Investigators and Chief Officers are restricted from registering claims
    if current_user.get("role") in ["investigator", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Role Restriction: Chief Compliance Officers and Senior Investigators are forensic adjudicators and oversight executives. Claim intake is strictly reserved for policyholders."
        )

    db = get_database()
    cid_count = db.claims.count_documents({}) + 1
    claim_id = f"CLM-2026-{cid_count:03d}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Alternating FIR logic: One time it agrees (corroborates), one time it disagrees (discrepancy) for uniformity
    is_discrepant_turn = (cid_count % 2 != 0)
    if payload.police_report:
        police_data = payload.police_report.model_dump()
    else:
        if is_discrepant_turn:
            police_data = {
                "station_name": "Indiranagar Traffic Police Station",
                "fir_gd_number": f"GD-{(cid_count * 73) % 900 + 100}/2026",
                "officer_name": "Sub-Inspector R. Ramesh",
                "police_summary": "Police General Diary (GD) records two-vehicle impact in active traffic lane with conflicting frontal deformation observed; notable divergence from driver initial statement at the scene.",
                "has_discrepancy": True,
                "corroboration_status": "Discrepancy Flagged"
            }
        else:
            police_data = {
                "station_name": "Indiranagar Traffic Police Station",
                "fir_gd_number": f"GD-{(cid_count * 73) % 900 + 100}/2026",
                "officer_name": "Sub-Inspector R. Ramesh",
                "police_summary": "Official Police GD entry corroborates policyholder declaration. On-scene physical inspection confirms stationary position at traffic signal with rear-end impact from trailing vehicle. Independent witnesses verify narrative.",
                "has_discrepancy": False,
                "corroboration_status": "Corroborated"
            }

    new_claim = {
        "claim_id": claim_id,
        "title": f"Incident at {payload.incident_location} ({payload.vehicle.make} {payload.vehicle.model})",
        "scenario_type": "user_submitted",
        "status": "pending_investigation",
        "priority": "medium",
        "priority_score": 55.0,
        "claimant": payload.claimant.model_dump(),
        "vehicle_reg": payload.vehicle.registration,
        "vehicle_image_url": payload.vehicle_image_url,
        "image_url": payload.vehicle_image_url,
        "policy_number": payload.policy_number,
        "incident_date": payload.incident_date,
        "incident_time": payload.incident_time,
        "incident_location": payload.incident_location,
        "accident_type": payload.accident_type,
        "reported_narrative": payload.reported_narrative,
        "estimated_damage": payload.estimated_damage,
        "third_party": payload.third_party,
        "police_report": police_data,
        "assigned_investigator": "usr-inv-01",
        "created_at": now,
        "updated_at": now
    }
    db.claims.insert_one(new_claim)

    # Insert vehicle record
    db.vehicles.insert_one({
        "vehicle_id": f"VEH-{claim_id}",
        "claim_id": claim_id,
        "registration_number": payload.vehicle.registration,
        "vin": payload.vehicle.vin or f"VIN{claim_id}",
        "make": payload.vehicle.make,
        "model": payload.vehicle.model,
        "year": payload.vehicle.year,
        "color": payload.vehicle.color or "Unspecified",
        "body_type": payload.vehicle.body_type or "Sedan",
        "image_url": payload.vehicle_image_url,
        "created_at": now
    })

    # Ingest consumer uploaded photograph, police file extract, and consumer statement into forensic evidence
    uploaded_photo_name = payload.photo_attachments[0] if (payload.photo_attachments and len(payload.photo_attachments) > 0) else "uploaded_vehicle_damage_photo.jpg"
    ev_photos = {
        "evidence_id": f"EVD-{claim_id}-1",
        "claim_id": claim_id,
        "file_name": uploaded_photo_name,
        "file_type": "image",
        "source": f"Policyholder Direct Upload ({payload.claimant.name})",
        "file_size": "3.8 MB",
        "storage_path": payload.vehicle_image_url or "/static/uploads/default_damage.jpg",
        "sha256_hash": f"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "notes": ["Exterior vehicle damage photograph submitted directly by policyholder."],
        "created_at": now
    }
    ev_police = {
        "evidence_id": f"EVD-{claim_id}-2",
        "claim_id": claim_id,
        "file_name": f"police_gd_extract_{police_data['fir_gd_number'].replace('/', '_')}.pdf",
        "file_type": "document",
        "source": f"Official Police Station Extract ({police_data['station_name']})",
        "file_size": "1.4 MB",
        "sha256_hash": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
        "notes": [
            f"Official Station GD Extract #{police_data['fir_gd_number']}",
            f"Attending Officer: {police_data['officer_name']}",
            f"Officer remarks: {police_data.get('police_summary') or 'Conflicting impact observations recorded at scene.'}"
        ],
        "created_at": now
    }
    ev_statement = {
        "evidence_id": f"EVD-{claim_id}-3",
        "claim_id": claim_id,
        "file_name": "claimant_sworn_declaration.pdf",
        "file_type": "statement",
        "source": "Consumer First Notice of Loss",
        "file_size": "420 KB",
        "sha256_hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        "notes": [f"Reported narrative: '{payload.reported_narrative}'"],
        "created_at": now
    }
    db.evidence.insert_many([ev_photos, ev_police, ev_statement])

    # Insert attending police officer witness statement into dossier
    db.witness_statements.insert_one({
        "statement_id": f"WIT-{claim_id}-POLICE",
        "claim_id": claim_id,
        "witness_name": police_data["officer_name"],
        "witness_type": "Attending Police Officer",
        "statement_text": police_data.get("police_summary") or "Police arrival at scene documented impact inconsistent with stationary rear-only collision.",
        "credibility_score": 0.95,
        "created_at": now
    })

    # Create Initial Investigation Report (Pending Executive Officer AI Inference)
    is_high_impact = payload.estimated_damage >= 500000
    db.investigation_reports.insert_one({
        "report_id": f"RPT-{claim_id}",
        "claim_id": claim_id,
        "title": f"Investigation Intelligence Report: {claim_id}",
        "status": "pending_investigation",
        "is_investigated": False,
        "is_high_impact": is_high_impact,
        "requires_executive_verification": is_high_impact,
        "settlement_calculation": {
            "eligible_repair": payload.estimated_damage,
            "deductible": 2000,
            "depreciation_deduction": payload.estimated_damage * 0.15,
            "salvage_allowance": 1000,
            "indicative_payout": max(0, payload.estimated_damage * 0.85 - 3000),
            "currency": "INR",
            "policy_clause": "Section 2.B (Subject to Executive AI Investigation)"
        },
        "executive_summary": (
            f"Consumer intake dossier submitted for {payload.vehicle.year} {payload.vehicle.make} {payload.vehicle.model}. "
            f"Awaiting Executive Officer AI Inference for YOLO damage localization and Police GD corroboration."
        ),
        "generated_by": "CLAIMSIGHT Autonomous Engine v3.1",
        "created_at": now
    })

    # Log initial timeline
    db.investigation_timelines.insert_one({
        "timeline_id": f"TIME-{claim_id}-0",
        "claim_id": claim_id,
        "event_type": "claim_registered",
        "event_timestamp": now,
        "timestamp_type": "upload_time",
        "description": "Consumer claim intake submitted with uploaded damage photograph.",
        "source_reference": "Consumer Intake Portal",
        "is_uncertain": False,
        "created_at": now
    })

    AuditService.log(claim_id, current_user["user_id"], "CLAIM_CREATED", f"Consumer claim {claim_id} filed for {payload.vehicle.registration}")

    new_claim.pop("_id", None)
    return new_claim

    # Log initial timeline
    db.investigation_timelines.insert_one({
        "timeline_id": f"TIME-{claim_id}-0",
        "claim_id": claim_id,
        "event_type": "claim_registered",
        "event_timestamp": now,
        "timestamp_type": "upload_time",
        "description": "Claim intake initiated with Consumer File and Police GD details ingested.",
        "source_reference": "Intake Portal",
        "is_uncertain": False,
        "created_at": now
    })

    AuditService.log(claim_id, current_user["user_id"], "CLAIM_CREATED", f"Claim {claim_id} created for {payload.vehicle.registration} with Police GD extract")

    new_claim.pop("_id", None)
    return new_claim

@router.get("/{claim_id}")
def get_claim(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id}, {"_id": 0})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    # If claimant role, verify ownership strictly
    if current_user.get("role") == "claimant":
        claimant_email = claim.get("claimant", {}).get("email", "").lower()
        if claimant_email != current_user.get("email", "").lower():
            raise HTTPException(
                status_code=403,
                detail="Unauthorized access: Policyholders may only view their own registered claims."
            )

    # Attach related vehicle, policy, evidence and stats
    vehicle = db.vehicles.find_one({"claim_id": claim_id}, {"_id": 0})
    policy = db.policies.find_one({"policy_number": claim.get("policy_number")}, {"_id": 0})
    evidence = list(db.evidence.find({"claim_id": claim_id}, {"_id": 0}).sort("created_at", -1))
    contradiction_count = db.evidence_relationships.count_documents({"claim_id": claim_id, "relationship_type": "Contradicts"})
    decision = db.investigator_decisions.find_one({"claim_id": claim_id}, {"_id": 0})

    return {
        "claim": claim,
        "vehicle": vehicle,
        "policy": policy,
        "evidence": evidence,
        "evidence_count": len(evidence),
        "contradiction_count": contradiction_count,
        "decision": decision
    }

@router.patch("/{claim_id}")
def update_claim(claim_id: str, payload: ClaimUpdate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    res = db.claims.update_one({"claim_id": claim_id}, {"$set": update_data})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Claim not found")

    AuditService.log(claim_id, current_user["user_id"], "CLAIM_UPDATED", f"Updated fields: {list(update_data.keys())}")
    return {"message": "Claim updated successfully", "updated_fields": update_data}

@router.delete("/{claim_id}", dependencies=[Depends(require_roles("admin"))])
def delete_claim(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    db.claims.delete_one({"claim_id": claim_id})
    AuditService.log(claim_id, current_user["user_id"], "CLAIM_DELETED", f"Claim {claim_id} deleted by Admin")
    return {"message": f"Claim {claim_id} deleted successfully"}

