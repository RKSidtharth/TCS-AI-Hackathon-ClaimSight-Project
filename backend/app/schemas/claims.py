from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class VehicleInfo(BaseModel):
    registration: str
    make: str
    model: str
    year: int
    vin: Optional[str] = None
    color: Optional[str] = None
    body_type: Optional[str] = "Sedan"

class ClaimantInfo(BaseModel):
    name: str
    phone: str
    email: str

class PoliceReportInput(BaseModel):
    station_name: Optional[str] = "Indiranagar Traffic Police Station"
    fir_gd_number: Optional[str] = "GD-482/2026"
    officer_name: Optional[str] = "Sub-Inspector R. Ramesh"
    police_summary: Optional[str] = None
    has_discrepancy: Optional[bool] = True

class ClaimCreate(BaseModel):
    policy_number: str
    claimant: ClaimantInfo
    vehicle: VehicleInfo
    incident_date: str
    incident_time: str
    incident_location: str
    accident_type: str
    reported_narrative: str
    estimated_damage: float
    third_party: Optional[str] = "None"
    police_report: Optional[PoliceReportInput] = None
    photo_attachments: Optional[List[str]] = None
    vehicle_image_url: Optional[str] = None

class ClaimUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_investigator: Optional[str] = None
    notes: Optional[str] = None

class ClaimOut(BaseModel):
    claim_id: str
    title: Optional[str] = None
    scenario_type: Optional[str] = None
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

class ClaimListResponse(BaseModel):
    total: int
    page: int
    limit: int
    claims: List[Dict[str, Any]]

