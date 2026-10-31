export interface User {
  user_id: string;
  name: string;
  email: string;
  role: 'admin' | 'investigator' | 'claimant';
  department?: string;
}

export interface Claim {
  claim_id: string;
  title: string;
  scenario_type: string;
  status: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  priority_score: number;
  claimant: {
    name: string;
    phone: string;
    email: string;
  };
  vehicle_reg: string;
  policy_number: string;
  incident_date: string;
  incident_time: string;
  incident_location: string;
  accident_type: string;
  reported_narrative: string;
  estimated_damage: number;
  third_party?: string;
  assigned_investigator?: string;
  vehicle_image_url?: string;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Vehicle {
  vehicle_id: string;
  claim_id: string;
  registration_number: string;
  vin: string;
  make: string;
  model: string;
  year: number;
  color: string;
  body_type: string;
}

export interface Policy {
  policy_id: string;
  claim_id: string;
  policy_number: string;
  holder_name: string;
  coverage_type: string;
  effective_from: string;
  effective_to: string;
  deductible_amount: number;
  sum_insured_limit: number;
  depreciation_waiver: boolean;
  status: string;
}

export interface EvidenceItem {
  evidence_id: string;
  claim_id: string;
  file_name: string;
  original_name?: string;
  file_type: 'image' | 'document' | 'estimate' | 'statement';
  source: string;
  file_size?: string;
  sha256_hash: string;
  storage_path: string;
  status: string;
  notes?: string[];
  is_duplicate?: boolean;
  duplicate_of?: string;
  exif_metadata?: {
    has_exif?: boolean;
    timestamp?: string;
    make?: string;
    model?: string;
    has_gps?: boolean;
  };
  created_at: string;
}

export interface Contradiction {
  conflict_id: string;
  category: string;
  severity: 'Low' | 'Medium' | 'High' | 'Critical';
  sources_involved: string[];
  description: string;
  materiality: string;
  alternative_explanations: string[];
  resolution_evidence: string;
}

export interface Hypothesis {
  hypothesis_id: string;
  title: string;
  support_level: string;
  probability_score: number;
  summary: string;
  supporting_evidence: string[];
  contradicting_evidence: string[];
  assumptions: string[];
}

export interface EvaluationDimension {
  status: string;
  score: number;
  details: string;
  uncertainty?: string;
  supporting_evidence?: string[];
  conflicting_evidence?: string[];
}

export interface ClaimEvaluation {
  evaluation_id: string;
  claim_id: string;
  physical_plausibility: EvaluationDimension;
  environmental_feasibility: EvaluationDimension;
  damage_consistency: EvaluationDimension;
  repair_anomaly: EvaluationDimension;
  overall_integrity_rating: string;
  investigation_priority_score: number;
}

export interface NextBestEvidenceRecommendation {
  request_id: string;
  claim_id: string;
  action_recommended: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  uncertainty_addressed: string;
  expected_information_gain: number;
  materiality: number;
  reliability: number;
  estimated_cost: number;
  rank_score: number;
  status: 'pending' | 'sent' | 'submitted' | 'reviewed' | 'rejected' | 'completed';
  responsible_party: string;
  hypotheses_distinguished?: string[];
}

export interface SettlementRecommendation {
  claim_id: string;
  policy_number: string;
  applicable_version: string;
  eligible_repair_amount: number;
  deductible: number;
  depreciation_deduction: number;
  salvage_allowance: number;
  indicative_settlement: number;
  currency: string;
  policy_clause_citations: Array<{ clause: string; text: string }>;
  investigator_approval_required: boolean;
}

export interface TimelineEvent {
  timeline_id: string;
  claim_id: string;
  event_type: string;
  event_timestamp: string;
  timestamp_type: 'event_time' | 'document_time' | 'upload_time' | 'ai_inference_time';
  description: string;
  source_reference: string;
  is_uncertain: boolean;
}

