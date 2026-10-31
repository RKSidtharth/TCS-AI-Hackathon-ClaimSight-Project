"""
CLAIMSIGHT AI - Evidence Intake & Management Endpoints
"""

import os
import datetime
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.core.database import get_database
from app.auth.security import get_current_user
from app.services.storage_service import StorageService
from app.services.audit_service import AuditService
from app.ai.next_best_evidence.recommendation_ranker import NextBestEvidenceRanker
from app.ai.computer_vision.damage_analyzer import ComputerVisionDamageAnalyzer
from app.ai.document_intelligence.ocr_pipeline import DocumentIntelligenceEngine

router = APIRouter(tags=["Evidence"])

@router.get("/claims/{claim_id}/evidence")
def list_claim_evidence(claim_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    items = list(db.evidence.find({"claim_id": claim_id}, {"_id": 0}).sort("created_at", -1))
    return {"claim_id": claim_id, "total": len(items), "evidence": items}

@router.post("/claims/{claim_id}/evidence", status_code=status.HTTP_201_CREATED)
async def upload_evidence(
    claim_id: str,
    file: UploadFile = File(...),
    notes: str = Form(None),
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    claim = db.claims.find_one({"claim_id": claim_id})
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Cannot upload empty file")

    # Persist file with SHA-256 and EXIF extraction
    storage_res = StorageService.save_file(
        filename=file.filename,
        content=content,
        claim_id=claim_id,
        uploader=current_user["user_id"]
    )

    ev_id = f"EVD-{claim_id}-{int(datetime.datetime.now().timestamp() * 1000)}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    note_list = [n.strip() for n in notes.split(",")] if notes else []

    evidence_doc = {
        "evidence_id": ev_id,
        "claim_id": claim_id,
        "file_name": storage_res["file_name"],
        "original_name": storage_res["original_name"],
        "file_type": storage_res["file_type"],
        "source": f"Upload by {current_user.get('name', 'User')}",
        "file_size": storage_res["file_size"],
        "sha256_hash": storage_res["sha256_hash"],
        "storage_path": storage_res["storage_path"],
        "status": "processing",
        "is_duplicate": storage_res["is_duplicate"],
        "duplicate_of": storage_res["duplicate_of"],
        "notes": note_list,
        "exif_metadata": storage_res["exif"],
        "created_at": now
    }
    db.evidence.insert_one(evidence_doc)

    # Perform immediate AI feature extraction
    abs_path = os.path.join(StorageService.get_upload_dir(), storage_res["file_name"])
    if storage_res["file_type"] == "image":
        cv_res = ComputerVisionDamageAnalyzer.analyze_image(abs_path)
        if cv_res.get("status") == "success":
            for det in cv_res.get("detections", []):
                db.extracted_facts.insert_one({
                    "fact_id": f"FACT-CV-{ev_id}",
                    "claim_id": claim_id,
                    "evidence_id": ev_id,
                    "category": "computer_vision_damage",
                    "extracted_text": f"Detected {det['component']} - {det['damage_type']} (Severity: {det['severity']})",
                    "confidence_score": det["confidence"],
                    "verification_status": "unverified",
                    "created_at": now
                })
    else:
        doc_facts = DocumentIntelligenceEngine.extract_document_facts(
            doc_type=storage_res["file_type"],
            text_content=" ".join(note_list) or file.filename,
            evidence_id=ev_id
        )
        for f in doc_facts:
            f["claim_id"] = claim_id
            f["created_at"] = now
            db.extracted_facts.insert_one(f)

    # Trigger Autonomous Re-Investigation Loop
    NextBestEvidenceRanker.execute_reinvestigation_loop(claim_id, ev_id)

    AuditService.log(
        claim_id,
        current_user["user_id"],
        "EVIDENCE_UPLOADED",
        f"Uploaded {storage_res['original_name']} (SHA-256: {storage_res['sha256_hash'][:12]}...)"
    )

    evidence_doc.pop("_id", None)
    return {
        "message": "Evidence successfully ingested and processed through AI extraction pipeline.",
        "evidence": evidence_doc
    }

@router.get("/evidence/{evidence_id}")
def get_evidence_detail(evidence_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    ev = db.evidence.find_one({"evidence_id": evidence_id}, {"_id": 0})
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence item not found")
    facts = list(db.extracted_facts.find({"evidence_id": evidence_id}, {"_id": 0}))
    return {"evidence": ev, "extracted_facts": facts}

@router.get("/evidence/{evidence_id}/file")
def get_evidence_file(evidence_id: str):
    db = get_database()
    ev = db.evidence.find_one({"evidence_id": evidence_id})
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence item not found")

    upload_dir = StorageService.get_upload_dir()
    filepath = os.path.join(upload_dir, ev["file_name"])

    if not os.path.exists(filepath):
        # Fallback to local storage
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        filepath = os.path.join(base_dir, ev.get("storage_path", ""))

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Physical evidence file not found in storage")

    media_type = "image/jpeg" if ev["file_type"] == "image" else "application/pdf"
    return FileResponse(filepath, media_type=media_type, filename=ev["file_name"])

@router.delete("/evidence/{evidence_id}")
def delete_evidence(evidence_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    ev = db.evidence.find_one({"evidence_id": evidence_id})
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence item not found")

    claim_id = ev["claim_id"]
    db.evidence.delete_one({"evidence_id": evidence_id})
    db.extracted_facts.delete_many({"evidence_id": evidence_id})
    AuditService.log(claim_id, current_user["user_id"], "EVIDENCE_DELETED", f"Deleted evidence {evidence_id}")
    return {"message": "Evidence item deleted successfully"}

