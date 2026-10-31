from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GraphNode(BaseModel):
    id: str
    type: str  # evidence, fact, hypothesis, contradiction, outcome
    label: str
    category: str
    data: Dict[str, Any]
    position: Optional[Dict[str, float]] = None

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    type: str  # Supports, Contradicts, Corroborates, DerivedFrom, RequiresVerification
    animated: Optional[bool] = False
    style: Optional[Dict[str, Any]] = None

class RelationshipGraphResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    summary: Dict[str, Any]

class ContradictionOut(BaseModel):
    conflict_id: str
    category: str
    severity: str
    sources_involved: List[str]
    description: str
    materiality: str
    alternative_explanations: List[str]
    resolution_evidence: str

class HypothesisOut(BaseModel):
    hypothesis_id: str
    title: str
    support_level: str
    probability_score: float
    summary: str
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    assumptions: List[str]

class WitnessDivergenceOut(BaseModel):
    witnesses: List[Dict[str, Any]]
    agreements: List[str]
    divergences: List[Dict[str, Any]]
    clarification_questions: List[str]

