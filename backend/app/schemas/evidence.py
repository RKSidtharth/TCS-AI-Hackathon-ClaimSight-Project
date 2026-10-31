from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class EvidenceOut(BaseModel):
    evidence_id: str
    claim_id: str
    file_name: str
    file_type: str
    source: str
    file_size: Optional[str] = None
    sha256_hash: str
    storage_path: str
    status: str
    notes: Optional[List[str]] = []
    created_at: str

class UploadResponse(BaseModel):
    message: str
    evidence_id: str
    sha256_hash: str
    is_duplicate: bool
    duplicate_of: Optional[str] = None
    file_name: str

