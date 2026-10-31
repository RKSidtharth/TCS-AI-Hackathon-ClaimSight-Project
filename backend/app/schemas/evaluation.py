from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class MetricDimension(BaseModel):
    status: str
    score: float
    details: str
    uncertainty: Optional[str] = "Low"
    supporting_evidence: Optional[List[str]] = []
    conflicting_evidence: Optional[List[str]] = []

class FullEvaluationResponse(BaseModel):
    evaluation_id: str
    claim_id: str
    physical_plausibility: MetricDimension
    environmental_feasibility: MetricDimension
    damage_consistency: MetricDimension
    repair_anomaly: MetricDimension
    overall_integrity_rating: str
    investigation_priority_score: float

class CounterfactualRequest(BaseModel):
    assumption: str  # e.g., "Exclude front fender damage as pre-existing"
    excluded_evidence_ids: Optional[List[str]] = []
    hypothetical_adjustments: Optional[Dict[str, Any]] = {}

class CounterfactualResponse(BaseModel):
    scenario_id: str
    assumption: str
    affected_relationships: List[str]
    recalculated_hypotheses: List[Dict[str, Any]]
    settlement_difference: float
    new_indicative_payout: float
    explanation: str

