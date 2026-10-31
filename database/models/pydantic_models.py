"""
CLAIMSIGHT AI - Database Collection Models (Pydantic Representations)
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    user_id: str
    name: str
    email: str
    password_hash: str
    role: str  # admin, investigator, claimant
    department: Optional[str] = None
    active: bool = True
    created_at: str

class ClaimModel(BaseModel):
    claim_id: str
    title: str
    scenario_type: str
    status: str
    priority: str
    priority_score: float
    claimant: Dict[str, Any]
    vehicle_reg: str
    policy_number: str
    incident_date: str
    incident_time: str
    incident_location: str
    accident_type: str
    reported_narrative: str
    estimated_damage: float
    third_party: Optional[str] = None
    assigned_investigator: Optional[str] = None
    created_at: str
    updated_at: str

class VehicleModel(BaseModel):
    vehicle_id: str
    claim_id: str
    registration_number: str
    vin: str
    make: str
    model: str
    year: int
    color: str
    body_type: str
    created_at: str

class EvidenceModel(BaseModel):
    evidence_id: str
    claim_id: str
    file_name: str
    file_type: str
    source: str
    file_size: str
    sha256_hash: str
    storage_path: str
    status: str
    notes: List[str]
    created_at: str

