from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ReportOut(BaseModel):
    report_id: str
    claim_id: str
    title: str
    status: str
    executive_summary: str
    settlement_calculation: Dict[str, Any]
    generated_by: str
    created_at: str

class DecisionCreate(BaseModel):
    status: str  # approved, rejected, escalated, info_requested
    notes: str
    approved_settlement_amount: Optional[float] = None
    confirmed_contradictions: Optional[List[str]] = []
    dismissed_contradictions: Optional[List[str]] = []

class NoteCreate(BaseModel):
    note: str

