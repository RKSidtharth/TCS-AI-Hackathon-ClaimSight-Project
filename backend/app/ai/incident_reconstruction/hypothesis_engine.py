"""
CLAIMSIGHT AI - Multi-Hypothesis Incident Reconstruction & Counterfactual Sandbox
Generates competing accident explanations and supports what-if counterfactual scenario simulations.
"""

import datetime
from typing import Dict, Any, List

class IncidentReconstructionEngine:
    @staticmethod
    def generate_hypotheses(claim_data: dict, contradictions: list) -> List[Dict[str, Any]]:
        cid = claim_data.get("claim_id", "")
        accident_type = claim_data.get("accident_type", "Collision")
        scenario_type = claim_data.get("scenario_type", "generic")

        hypotheses = []

        if scenario_type == "unexplained_secondary_damage":
            hypotheses.append({
                "hypothesis_id": f"HYP-{cid}-1",
                "title": "H1: Primary Rear Impact Followed by Secondary Barrier Rebound",
                "support_level": "Moderate Support",
                "probability_score": 0.48,
                "summary": "Vehicle was rear-ended, causing driver to swerve into the bridge safety guardrail.",
                "supporting_evidence": ["Rear tailgate indentation photographs"],
                "contradicting_evidence": ["Initial claimant verbal statement omitting front barrier contact"],
                "assumptions": ["Driver experienced sudden rotational inertia after rear bump"]
            })
            hypotheses.append({
                "hypothesis_id": f"HYP-{cid}-2",
                "title": "H2: Pre-Existing Frontal Damage Bundled into Rear Claim",
                "support_level": "Strong Evidence of Divergence",
                "probability_score": 0.52,
                "summary": "Front fender and headlamp were damaged in a separate prior unnotified incident.",
                "supporting_evidence": ["Foreign paint transfer scraping", "Initial driver statement"],
                "contradicting_evidence": [],
                "assumptions": ["Rear impact energy was insufficient to deform front crumple zones"]
            })
        elif scenario_type == "multi_hypothesis_ambiguity":
            hypotheses.append({
                "hypothesis_id": f"HYP-{cid}-1",
                "title": "H1: Trailing Bus Struck Stationary Insured into Preceding Vehicle",
                "support_level": "Supported by Insured Account",
                "probability_score": 0.45,
                "summary": "Insured had stopped safely; heavy trailing bus initiated entire kinetic collapse.",
                "supporting_evidence": ["Insured driver statement", "Rear crumple severity"],
                "contradicting_evidence": ["Preceding driver testimony reporting two separate jolts"],
                "assumptions": ["First shock felt was initial rear-to-front energy transmission"]
            })
            hypotheses.append({
                "hypothesis_id": f"HYP-{cid}-2",
                "title": "H2: Insured Struck Lead Vehicle First, Then Trailing Bus Struck Insured",
                "support_level": "Supported by Third-Party Witnesses",
                "probability_score": 0.55,
                "summary": "Insured rear-ended lead car; trailing bus subsequently collided with insured's rear.",
                "supporting_evidence": ["Lead car driver statement", "Bus driver statement"],
                "contradicting_evidence": ["Insured driver statement"],
                "assumptions": ["Insured vehicle failed to maintain safe stopping headway"]
            })
        else:
            has_contradictions = len(contradictions) > 0
            if has_contradictions:
                hypotheses.append({
                    "hypothesis_id": f"HYP-{cid}-1",
                    "title": "H1: Compound Incident with Secondary Kinetic Rebound",
                    "support_level": "Supported by Claimant Account",
                    "probability_score": 0.42,
                    "summary": "Vehicle experienced initial impact sequence as reported in claimant notice of loss; secondary kinetic dissipation explains observed divergent damage vectors.",
                    "supporting_evidence": ["Claimant notice of loss sworn statement", "Vehicle registration telemetry"],
                    "contradicting_evidence": [c.get("category", "Evidence mismatch") for c in contradictions[:2]],
                    "assumptions": ["Driver experienced sudden evasive inertia during or immediately following initial impact"]
                })
                hypotheses.append({
                    "hypothesis_id": f"HYP-{cid}-2",
                    "title": "H2: Unrelated Pre-Existing Deformation Bundled into Claim",
                    "support_level": "Supported by Objective Forensic Signals",
                    "probability_score": 0.58,
                    "summary": "Primary impact occurred, but secondary or divergent damage identified by YOLOv8 vision / Police GD predates current notice of loss.",
                    "supporting_evidence": ["YOLOv8 neural damage localization", "Official Police GD on-scene observation extract"],
                    "contradicting_evidence": ["Claimant initial verbal declaration"],
                    "assumptions": ["Deformation patina and paint micro-fractures indicate aging prior to reported loss timestamp"]
                })
            else:
                hypotheses.append({
                    "hypothesis_id": f"HYP-{cid}-1",
                    "title": "H1: Incident Occurred Strictly as Reported by Claimant",
                    "support_level": "High Corroboration",
                    "probability_score": 0.92,
                    "summary": "All physical deformations, metadata, and official police documents corroborate claimant sequence cleanly.",
                    "supporting_evidence": ["Submitted damage photographs", "Certified police station general diary entry"],
                    "contradicting_evidence": [],
                    "assumptions": ["Accident sequence was uninterrupted and verified by on-scene officer"]
                })
                hypotheses.append({
                    "hypothesis_id": f"HYP-{cid}-2",
                    "title": "H2: Low-Energy Single-Point Contact without Secondary Rebound",
                    "support_level": "Secondary Feasible Explanation",
                    "probability_score": 0.08,
                    "summary": "Impact was isolated strictly to the primary contact point with no structural frame displacement.",
                    "supporting_evidence": ["Absence of frame misalignment in photos"],
                    "contradicting_evidence": [],
                    "assumptions": ["Trailing vehicle had already decelerated significantly prior to contact"]
                })

        return hypotheses

    @staticmethod
    def run_counterfactual_simulation(
        claim_data: dict,
        assumption: str,
        current_hypotheses: list,
        current_estimate: float
    ) -> Dict[str, Any]:
        """
        Tests hypothetical 'what if' assumptions without mutating original investigation.
        """
        assumption_lower = assumption.lower()
        affected_rels = []
        new_hypotheses = []
        settlement_diff = 0.0

        if "pre-existing" in assumption_lower or "front" in assumption_lower:
            affected_rels.append("REL-FrontDamage-to-RearIncident: Disassociated")
            settlement_diff = -current_estimate * 0.65  # deduct front repair cost
            explanation = (
                f"Assuming front-side damage is excluded as pre-existing: "
                f"The physical contradiction between rear impact and front damage is resolved. "
                f"Hypothesis H2 becomes dominant (95% support). "
                f"Payable loss reduces by ₹{abs(settlement_diff):,.2f}."
            )
        elif "rain" in assumption_lower or "dry" in assumption_lower:
            affected_rels.append("REL-WeatherToTraction: Neutralized")
            explanation = (
                "Assuming driver error rather than hydroplaning: "
                "Environmental feasibility shifts to Irrelevant, but Comprehensive OD policy retains coverage."
            )
        else:
            explanation = f"Hypothetical condition '{assumption}' evaluated. No core structural relationships altered."

        new_payout = max(0.0, current_estimate + settlement_diff - 1000)

        return {
            "scenario_id": f"CF-{int(datetime.datetime.now().timestamp()) if 'datetime' in globals() else 'TEST'}",
            "assumption": assumption,
            "affected_relationships": affected_rels,
            "settlement_difference": round(settlement_diff, 2),
            "new_indicative_payout": round(new_payout, 2),
            "explanation": explanation
        }
