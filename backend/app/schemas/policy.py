from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class PolicyOut(BaseModel):
    policy_id: str
    policy_number: str
    holder_name: str
    coverage_type: str
    effective_from: str
    effective_to: str
    deductible_amount: float
    sum_insured_limit: float
    depreciation_waiver: bool
    status: str

class SettlementRecommendationResponse(BaseModel):
    claim_id: str
    policy_number: str
    applicable_version: str
    eligible_repair_amount: float
    deductible: float
    depreciation_deduction: float
    salvage_allowance: float
    indicative_settlement: float
    currency: str
    policy_clause_citations: List[Dict[str, str]]
    investigator_approval_required: bool = True

