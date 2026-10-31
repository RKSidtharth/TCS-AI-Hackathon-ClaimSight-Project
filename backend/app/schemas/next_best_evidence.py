from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class RecommendationOut(BaseModel):
    request_id: str
    claim_id: str
    action_recommended: str
    priority: str
    uncertainty_addressed: str
    expected_information_gain: float
    materiality: float
    reliability: float
    estimated_cost: float
    rank_score: float
    status: str
    responsible_party: str

class EvidenceRequestCreate(BaseModel):
    action_recommended: str
    uncertainty_addressed: str
    priority: Optional[str] = "High"
    responsible_party: Optional[str] = "Claimant"
    notes: Optional[str] = None

class EvidenceRequestUpdate(BaseModel):
    status: str  # pending, sent, submitted, reviewed, rejected, completed
    notes: Optional[str] = None

