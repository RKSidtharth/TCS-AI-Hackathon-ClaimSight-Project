"""
CLAIMSIGHT AI - Narrative Extraction & NLP Semantic Parser
Separates stated facts from inferences, extracts impact trajectories and stated conditions.
"""

import re
from typing import Dict, Any, List

class NarrativeExtractor:
    @staticmethod
    def parse_narrative(text: str) -> Dict[str, Any]:
        lower = text.lower()

        # 1. Impact direction extraction
        impact_direction = "Unknown"
        if any(w in lower for w in ["behind", "rear", "back", "tailgate"]):
            impact_direction = "Rear-End (180 deg)"
        elif any(w in lower for w in ["head on", "front", "hood", "bumper"]):
            impact_direction = "Frontal Impact (0 deg)"
        elif any(w in lower for w in ["side", "t-bone", "tbone", "door", "fender", "right quarter", "left quarter"]):
            impact_direction = "Lateral / Side-Swipe (90 deg)"
        elif any(w in lower for w in ["ditch", "barrier", "divider", "guardrail"]):
            impact_direction = "Fixed Object / Roadway Departure"

        # 2. Movement state
        stationary = any(w in lower for w in ["stationary", "stopped", "red light", "parked", "halt"])
        motion_state = "Stationary / Halted" if stationary else "In Motion"

        # 3. Road conditions claimed
        wet_road = any(w in lower for w in ["rain", "wet", "hydroplan", "cloudburst", "water", "slip", "skid"])
        road_claim = "Wet / Reduced Friction" if wet_road else "Normal / Dry"

        # 4. Third-party involvement stated
        third_party_stated = any(w in lower for w in ["truck", "taxi", "car", "bus", "bike", "two-wheeler", "scooter", "vehicle"])

        # 5. Segregation of stated vs inferred
        stated_facts = [
            f"Impact vector declared: {impact_direction}",
            f"Vehicle operating status: {motion_state}",
            f"Roadway friction claimed: {road_claim}"
        ]
        inferred = []
        if stationary and impact_direction == "Rear-End (180 deg)":
            inferred.append("High probability of primary rear-end impact force transfer")
        if wet_road:
            inferred.append("Claim implies environmental mitigation for driver control failure")

        return {
            "impact_direction": impact_direction,
            "motion_state": motion_state,
            "road_condition_claimed": road_claim,
            "third_party_involved_stated": third_party_stated,
            "stated_facts": stated_facts,
            "inferred_information": inferred,
            "unknown_parameters": ["Exact delta-V velocity change", "Airbag deployment millisecond timestamp"]
        }

