"""
CLAIMSIGHT AI - Comprehensive Database Seed Data
Populates all 22 collections with realistic, interconnected synthetic data
for 10 motor insurance claim investigation scenarios.
"""

import os
import sys
import hashlib
import datetime
import bcrypt
import pymongo

# Add backend directory to sys.path to enable sample image generation
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
sys.path.insert(0, BACKEND_DIR)

try:
    from app.utils.sample_generator import create_sample_damage_image, create_sample_document_image
except ImportError:
    create_sample_damage_image = None
    create_sample_document_image = None


def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_database(uri: str = "mongodb://localhost:27017", db_name: str = "claimsight_ai", client=None):
    if client is None:
        client = pymongo.MongoClient(uri)
    db = client[db_name]
    print(f"[*] Seeding CLAIMSIGHT AI database '{db_name}'...")

    # Drop existing collections to ensure a clean, reproducible state
    for coll in [
        "users", "claims", "vehicles", "policies", "policy_versions", "evidence",
        "extracted_facts", "evidence_relationships", "witness_statements",
        "investigation_timelines", "accident_hypotheses", "claim_evaluations",
        "repair_estimates", "repair_benchmarks", "evidence_requests",
        "investigation_reports", "investigator_decisions", "audit_logs",
        "notifications", "model_registry", "external_data_records", "counterfactual_scenarios"
    ]:
        db[coll].delete_many({})

    # -------------------------------------------------------------
    # 1. USERS
    # -------------------------------------------------------------
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    users_data = [
        {
            "user_id": "usr-admin-01",
            "name": "Chief Compliance Officer",
            "email": "admin@claimsight.ai",
            "password_hash": hash_pw("ClaimsightAdmin2026!"),
            "role": "admin",
            "department": "Special Investigations Unit (SIU) Executive",
            "active": True,
            "created_at": now
        },
        {
            "user_id": "usr-inv-01",
            "name": "Senior SIU Investigator Sarah Chen",
            "email": "investigator@claimsight.ai",
            "password_hash": hash_pw("Investigator2026!"),
            "role": "investigator",
            "department": "Motor Physical Damage & Fraud Detection",
            "active": True,
            "created_at": now
        },
        {
            "user_id": "usr-claimant-01",
            "name": "Rajesh Kumar",
            "email": "claimant@claimsight.ai",
            "password_hash": hash_pw("Claimant2026!"),
            "role": "claimant",
            "department": "Policyholder",
            "active": True,
            "created_at": now
        }
    ]
    db.users.insert_many(users_data)
    print(f"  [OK] Seeded {len(users_data)} users.")

    # -------------------------------------------------------------
    # 2. MODEL REGISTRY
    # -------------------------------------------------------------
    models_data = [
        {
            "model_id": "mod-yolo-v8-dmg",
            "model_name": "YOLOv8-DamageDetect-Ensemble",
            "version": "v2.4.1",
            "modality": "computer_vision",
            "description": "Vehicle component identification and exterior physical damage detection",
            "active": True,
            "confidence_threshold": 0.65,
            "updated_at": now
        },
        {
            "model_id": "mod-doc-ocr-v2",
            "model_name": "PaddleOCR-DocumentIntelligence",
            "version": "v3.1.0",
            "modality": "document_intelligence",
            "description": "Multi-page policy, police report, and repair estimate tabular fact extractor",
            "active": True,
            "confidence_threshold": 0.80,
            "updated_at": now
        },
        {
            "model_id": "mod-nlp-contradiction",
            "model_name": "CrossModal-Consistency-Transformer",
            "version": "v4.0.2",
            "modality": "nlp_reasoning",
            "description": "Witness statement divergence analyzer and cross-modal contradiction detector",
            "active": True,
            "confidence_threshold": 0.75,
            "updated_at": now
        }
    ]
    db.model_registry.insert_many(models_data)
    print(f"  [OK] Seeded {len(models_data)} AI models in registry.")

    # -------------------------------------------------------------
    # 3. REPAIR BENCHMARKS
    # -------------------------------------------------------------
    benchmarks_data = [
        {"benchmark_id": "bmk-001", "make": "Honda", "model": "City", "component": "Rear Bumper Cover", "oem_price": 7500, "aftermarket_price": 4200, "labor_hours": 2.5, "paint_cost": 3200, "region": "North"},
        {"benchmark_id": "bmk-002", "make": "Honda", "model": "City", "component": "Tail Lamp RHS", "oem_price": 5200, "aftermarket_price": 3100, "labor_hours": 0.8, "paint_cost": 0, "region": "North"},
        {"benchmark_id": "bmk-003", "make": "Hyundai", "model": "Creta", "component": "Front Left Fender", "oem_price": 8900, "aftermarket_price": 5400, "labor_hours": 3.0, "paint_cost": 3800, "region": "South"},
        {"benchmark_id": "bmk-004", "make": "Hyundai", "model": "Creta", "component": "Headlamp Assembly LHS", "oem_price": 14200, "aftermarket_price": 8600, "labor_hours": 1.2, "paint_cost": 0, "region": "South"},
        {"benchmark_id": "bmk-005", "make": "Hyundai", "model": "Creta", "component": "Rear Bumper", "oem_price": 9500, "aftermarket_price": 5800, "labor_hours": 2.5, "paint_cost": 3500, "region": "South"},
        {"benchmark_id": "bmk-006", "make": "Maruti", "model": "Swift", "component": "Rear Right Door Panel", "oem_price": 11500, "aftermarket_price": 6800, "labor_hours": 4.0, "paint_cost": 4200, "region": "West"},
        {"benchmark_id": "bmk-007", "make": "Tata", "model": "Nexon EV", "component": "LED Headlamp LHS", "oem_price": 26500, "aftermarket_price": 16000, "labor_hours": 1.5, "paint_cost": 0, "region": "North"},
        {"benchmark_id": "bmk-008", "make": "Tata", "model": "Nexon EV", "component": "Front Bumper & Grille", "oem_price": 12800, "aftermarket_price": 8200, "labor_hours": 3.0, "paint_cost": 4000, "region": "North"},
        {"benchmark_id": "bmk-009", "make": "Mahindra", "model": "XUV700", "component": "Front Radar Module & Bumper", "oem_price": 38000, "aftermarket_price": 24000, "labor_hours": 5.0, "paint_cost": 5000, "region": "South"},
        {"benchmark_id": "bmk-010", "make": "Toyota", "model": "Innova Crysta", "component": "Right Front Fender & Door", "oem_price": 22000, "aftermarket_price": 14000, "labor_hours": 6.0, "paint_cost": 7500, "region": "South"},
        {"benchmark_id": "bmk-011", "make": "BMW", "model": "3 Series", "component": "Adaptive Laser Headlamp RHS & Front Clip", "oem_price": 195000, "aftermarket_price": 120000, "labor_hours": 8.0, "paint_cost": 18000, "region": "North"},
        {"benchmark_id": "bmk-012", "make": "Mercedes-Benz", "model": "E-Class", "component": "Front Axle Subframe & Air Suspension", "oem_price": 340000, "aftermarket_price": 210000, "labor_hours": 14.0, "paint_cost": 22000, "region": "West"},
        {"benchmark_id": "bmk-013", "make": "Audi", "model": "Q5", "component": "Matrix LED Headlamp & Front Radar Bumper", "oem_price": 225000, "aftermarket_price": 145000, "labor_hours": 9.0, "paint_cost": 19000, "region": "South"}
    ]
    db.repair_benchmarks.insert_many(benchmarks_data)
    print(f"  [OK] Seeded {len(benchmarks_data)} dynamic repair benchmarks.")

    # -------------------------------------------------------------
    # 4. TEN RICH SCENARIOS
    # -------------------------------------------------------------
    scenarios = [
        # SCENARIO 1: Consistent accident with matching evidence
        {
            "claim_id": "CLM-2026-001",
            "title": "Consistent Rear Impact Collision at Traffic Intersection",
            "scenario_type": "consistent_accident",
            "status": "investigation_completed",
            "priority": "low",
            "priority_score": 22.5,
            "claimant": {"name": "Rajesh Kumar", "phone": "+91 98765 43210", "email": "claimant@claimsight.ai"},
            "vehicle": {
                "vehicle_id": "VEH-001", "registration": "DL-01-AB-1234", "vin": "MA3EWD81S00192841",
                "make": "Honda", "model": "City VX", "year": 2022, "color": "Lunar Silver", "body_type": "Sedan"
            },
            "policy": {
                "policy_id": "POL-001", "policy_number": "POL-HND-2025-8812",
                "holder": "Rajesh Kumar", "coverage_type": "Comprehensive Zero-Depreciation",
                "start_date": "2025-06-01T00:00:00Z", "end_date": "2026-05-31T23:59:59Z",
                "deductible": 1000, "coverage_limit": 1150000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-10", "time": "18:45:00",
                "location": "MG Road Crossing near Trinity Circle, Bengaluru",
                "accident_type": "Rear-End Collision",
                "damage_estimate": 24500,
                "third_party": "Maruti Dzire (KA-03-MM-4491)",
                "narrative": "I was stationary at a red traffic signal when a trailing commercial taxi failed to brake in time and impacted my rear bumper and cracked the right tail lamp."
            },
            "evidence_items": [
                {"id": "EVD-001-1", "name": "rear_bumper_damage.jpg", "type": "image", "source": "Claimant Upload", "size": "3.2 MB", "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "notes": ["Crushed rear bumper cover", "Impact fractures right tail lamp"]},
                {"id": "EVD-001-2", "name": "police_gd_entry_extract.pdf", "type": "document", "source": "Bengaluru Traffic Police", "size": "1.1 MB", "hash": "7a35c91b5e8284f18b45f36e492161726a457d81a942a49281a17b8f9e11c841", "notes": ["Stationary vehicle struck from rear", "Zero injuries", "GD No. 441/2026"]},
                {"id": "EVD-001-3", "name": "authorized_honda_estimate.pdf", "type": "estimate", "source": "Dakshin Honda Bodyshop", "size": "850 KB", "hash": "19b48c3b44b82d718a245582f6e729a73e4492b118a1a441e8b284917a22e841", "notes": ["Bumper replacement ₹7,500", "Tail lamp RHS ₹5,200", "Paint & Labor ₹11,800"]}
            ],
            "contradictions": [],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-001-A",
                    "title": "Reported Stationary Rear-End Impact",
                    "support_level": "Highly Supported",
                    "probability_score": 0.94,
                    "summary": "Vehicle was stationary at traffic signal and struck squarely by trailing vehicle, entirely consistent with physical deformation and police report.",
                    "supporting_evidence": ["EVD-001-1", "EVD-001-2", "EVD-001-3"],
                    "contradicting_evidence": [],
                    "assumptions": ["Braking distance of trailing vehicle insufficient on wet pavement"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent", "score": 96, "details": "Impact deformation depth (65mm) and horizontal bumper indentation strictly match stationary low-speed rear impact (18-22 km/h)."},
                "environmental_feasibility": {"status": "Verified", "score": 94, "details": "Bengaluru MG Road weather confirmed overcast with 2.1mm rainfall at 18:45, matching reduced road friction."},
                "damage_consistency": {"status": "Aligned", "score": 95, "details": "Observed damage confined solely to rear bumper cover, mounting brackets, and RHS tail lamp cluster."},
                "repair_anomaly": {"status": "Normal", "score": 98, "details": "Quoted repair cost (₹24,500) within 3.5% of regional Honda benchmark average."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-001-1",
                    "action": "Request Final Bodyshop Delivery & Invoice Receipt",
                    "priority": "Low",
                    "uncertainty_addressed": "Post-repair validation and parts replacement verification",
                    "expected_information_gain": 0.35,
                    "materiality": 0.40,
                    "reliability": 0.95,
                    "cost": 0.10,
                    "rank_score": 1.33,
                    "status": "pending",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 24500,
                "deductible": 1000,
                "depreciation_deduction": 0,
                "salvage_allowance": 500,
                "indicative_payout": 23000,
                "currency": "INR",
                "policy_clause": "Section 1.A (Own Damage Loss Waiver) - Full coverage applicable with zero depreciation add-on."
            }
        },

        # SCENARIO 2: Rear collision with additional front-side damage
        {
            "claim_id": "CLM-2026-002",
            "title": "Rear Collision with Unexplained Front-Left Wing Damage",
            "scenario_type": "unexplained_secondary_damage",
            "status": "investigation_active",
            "priority": "high",
            "priority_score": 78.4,
            "claimant": {"name": "Pooja Sharma", "phone": "+91 91234 56789", "email": "pooja.sharma@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-002", "registration": "KA-05-NB-9812", "vin": "MALC481CLPM019284",
                "make": "Hyundai", "model": "Creta SX", "year": 2023, "color": "Polar White", "body_type": "SUV"
            },
            "policy": {
                "policy_id": "POL-002", "policy_number": "POL-HYU-2025-4190",
                "holder": "Pooja Sharma", "coverage_type": "Comprehensive",
                "start_date": "2025-08-15T00:00:00Z", "end_date": "2026-08-14T23:59:59Z",
                "deductible": 2000, "coverage_limit": 1450000, "depreciation_waiver": False
            },
            "incident": {
                "date": "2026-03-12", "time": "21:15:00",
                "location": "Outer Ring Road flyover, Marathahalli, Bengaluru",
                "accident_type": "Reported Single-Point Rear Impact",
                "damage_estimate": 82000,
                "third_party": "Unknown heavy vehicle that fled",
                "narrative": "A speeding delivery truck struck my car from behind while slowing down for flyover traffic. The force jolted me forward."
            },
            "evidence_items": [
                {"id": "EVD-002-1", "name": "rear_creta_dent.jpg", "type": "image", "source": "Claimant Smartphone", "size": "2.8 MB", "hash": "91a8c3e411b98a7281a44e912781a942b49281a17b8f9e11c84119b48c3b44b8", "notes": ["Moderate dent in tailgate and rear lower bumper fascia"]},
                {"id": "EVD-002-2", "name": "front_left_fender_damage.jpg", "type": "image", "source": "Bodyshop Intake", "size": "3.5 MB", "hash": "44b82d718a245582f6e729a73e4492b118a1a441e8b284917a22e84191a8c3e4", "notes": ["Severe crumpling on LHS front fender", "Shattered LHS LED projector headlamp", "Paint transfer blue/yellow"]},
                {"id": "EVD-002-3", "name": "claimant_first_statement.pdf", "type": "statement", "source": "Intake Audio Transcript", "size": "340 KB", "hash": "f6e729a73e4492b118a1a441e8b284917a22e84191a8c3e444b82d718a245582", "notes": ["Claimant explicitly stated: 'Only rear was struck. No other vehicle was touched in front.'"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-002-1",
                    "category": "Physical Damage vs Narrative Divergence",
                    "severity": "High",
                    "sources_involved": ["EVD-002-2 (Photos)", "EVD-002-3 (Narrative)"],
                    "description": "Claimant statement declares zero frontal contact and sole rear impact, yet front-left fender and headlamp sustained heavy structural crumple and distinct two-tone paint transfer.",
                    "materiality": "Material - Front damage accounts for ₹52,000 of ₹82,000 estimate.",
                    "alternative_explanations": ["Secondary rebound impact into flyover safety guardrail", "Pre-existing frontal damage combined into this claim"],
                    "resolution_evidence": "Inspect flyover median crash barrier for corresponding blue/yellow paint scrapings."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-002-A",
                    "title": "Secondary Rebound Collision with Guardrail",
                    "support_level": "Moderate Support",
                    "probability_score": 0.48,
                    "summary": "Vehicle was rear-ended, driver panicked and swerved left into the bridge barrier.",
                    "supporting_evidence": ["EVD-002-1", "EVD-002-2"],
                    "contradicting_evidence": ["EVD-002-3"],
                    "assumptions": ["Driver omitted barrier contact due to fear of contributory negligence"]
                },
                {
                    "hypothesis_id": "HYP-002-B",
                    "title": "Pre-Existing Frontal Damage Bundling",
                    "support_level": "Strong Evidence of Divergence",
                    "probability_score": 0.52,
                    "summary": "Front fender damage occurred prior to this incident and is improperly bundled into this rear-end claim.",
                    "supporting_evidence": ["EVD-002-3"],
                    "contradicting_evidence": [],
                    "assumptions": ["Paint transfer colors do not match any vehicle involved in the rear collision"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Potentially Inconsistent", "score": 45, "details": "Rear impact vector (180 degrees) cannot mechanically generate front-left lateral compression without secondary obstruction."},
                "environmental_feasibility": {"status": "Verified", "score": 88, "details": "Dry road surface, good street lighting at Marathahalli flyover."},
                "damage_consistency": {"status": "Discrepant", "score": 38, "details": "Significant directional contradiction between rear kinetic energy and front-side deformation."},
                "repair_anomaly": {"status": "Review Required", "score": 62, "details": "63% of claimed repair cost belongs to front section not described in incident narrative."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-002-1",
                    "action": "Request Front Impact Absorber & Chassis Alignment Inspection",
                    "priority": "Critical",
                    "uncertainty_addressed": "Differentiates secondary barrier rebound from separate prior collision",
                    "expected_information_gain": 0.88,
                    "materiality": 0.85,
                    "reliability": 0.92,
                    "cost": 0.20,
                    "rank_score": 2.29,
                    "status": "sent",
                    "responsible": "Investigator"
                },
                {
                    "rec_id": "REC-002-2",
                    "action": "Inspect Marathahalli Flyover CCTV Footage (21:00-21:30)",
                    "priority": "High",
                    "uncertainty_addressed": "Validates whether third-party heavy truck struck vehicle or if swerve occurred",
                    "expected_information_gain": 0.92,
                    "materiality": 0.90,
                    "reliability": 0.95,
                    "cost": 0.40,
                    "rank_score": 1.57,
                    "status": "pending",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 30000,
                "deductible": 2000,
                "depreciation_deduction": 4500,
                "salvage_allowance": 800,
                "indicative_payout": 22700,
                "currency": "INR",
                "policy_clause": "Clause 4.B: Damage unrelated to the proximate cause of the notified event is excluded pending substantiation."
            }
        },

        # SCENARIO 3: Possible pre-existing vehicle damage
        {
            "claim_id": "CLM-2026-003",
            "title": "Oxidized Rust Patina on Claimed Fresh Side Impact",
            "scenario_type": "pre_existing_damage",
            "status": "investigation_active",
            "priority": "high",
            "priority_score": 82.1,
            "claimant": {"name": "Arjun Mehta", "phone": "+91 99887 76655", "email": "arjun.mehta@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-003", "registration": "MH-02-CD-5678", "vin": "MA3FBB01S00849201",
                "make": "Maruti", "model": "Swift ZXi", "year": 2020, "color": "Magma Grey", "body_type": "Hatchback"
            },
            "policy": {
                "policy_id": "POL-003", "policy_number": "POL-MAR-2025-1029",
                "holder": "Arjun Mehta", "coverage_type": "Comprehensive",
                "start_date": "2025-04-10T00:00:00Z", "end_date": "2026-04-09T23:59:59Z",
                "deductible": 1500, "coverage_limit": 580000, "depreciation_waiver": False
            },
            "incident": {
                "date": "2026-03-15", "time": "14:20:00",
                "location": "Andheri West Market parking lot, Mumbai",
                "accident_type": "Side Swipe While Parked",
                "damage_estimate": 32000,
                "third_party": "Unknown parked vehicle",
                "narrative": "I parked my Swift for 45 minutes; upon returning, the rear right door panel had a deep dent and severe scrape."
            },
            "evidence_items": [
                {"id": "EVD-003-1", "name": "right_door_panel_macro.jpg", "type": "image", "source": "Field Inspection", "size": "4.1 MB", "hash": "849201ma3fbb01se3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934c", "notes": ["Deep rust corrosion along crease", "Flaking oxidized base coat", "Fresh superficial dust wipe"]},
                {"id": "EVD-003-2", "name": "claim_form_declaration.pdf", "type": "document", "source": "Claimant Portal", "size": "480 KB", "hash": "e11c84119b48c3b44b82d718a245582f6e729a73e4492b118a1a441e8b284917", "notes": ["Incident occurred March 15, claim filed March 16"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-003-1",
                    "category": "Chronological Inconsistency in Physical Aging",
                    "severity": "High",
                    "sources_involved": ["EVD-003-1 (Macro Photo)", "EVD-003-2 (Claim Form)"],
                    "description": "Exposed steel inside the door panel crease exhibits advanced iron oxide (rust) crusting and paint micro-delamination, which requires 3-6 weeks of atmospheric exposure. Claim asserts incident occurred 24 hours prior.",
                    "materiality": "Material - Claims full door skin replacement (₹18,500) for old lesion.",
                    "alternative_explanations": ["A fresh minor contact occurred over a previously un-repaired rusty indentation", "Claimant was unaware of rust under previous scrape"],
                    "resolution_evidence": "Obtain prior year renewal inspection photos or service bay check-in log."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-003-A",
                    "title": "Aggravation of Pre-Existing Corrosion Damage",
                    "support_level": "Strong Evidence of Pre-Existing Damage",
                    "probability_score": 0.78,
                    "summary": "Vehicle had an un-repaired oxidized dent from months ago; parking contact merely added superficial scuffing.",
                    "supporting_evidence": ["EVD-003-1"],
                    "contradicting_evidence": ["EVD-003-2"],
                    "assumptions": ["Rust cannot form in 24 hours even in humid coastal environment"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Potentially Inconsistent", "score": 32, "details": "Corrosion kinetics contradict acute trauma reported within past 24 hours."},
                "environmental_feasibility": {"status": "Verified", "score": 85, "details": "Mumbai coastal climate accelerates oxidation, but 24 hours remains chemically impossible for layered rust crust."},
                "damage_consistency": {"status": "Discrepant", "score": 28, "details": "Metallurgical rust layer proves damage pre-dates the reported March 15 incident."},
                "repair_anomaly": {"status": "Review Required", "score": 50, "details": "Full replacement quoted rather than paint touch-up of acute scrape."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-003-1",
                    "action": "Retrieve Previous Policy Year Vehicle Inspection Photos (April 2025)",
                    "priority": "High",
                    "uncertainty_addressed": "Decisively establishes if right door dent existed at policy inception",
                    "expected_information_gain": 0.95,
                    "materiality": 0.88,
                    "reliability": 0.98,
                    "cost": 0.10,
                    "rank_score": 4.10,
                    "status": "pending",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 4500,
                "deductible": 1500,
                "depreciation_deduction": 800,
                "salvage_allowance": 0,
                "indicative_payout": 2200,
                "currency": "INR",
                "policy_clause": "Exclusion Clause 2.1: Pre-existing defects, corrosion, wear-and-tear, or damages predating policy inception are not covered."
            }
        },

        # SCENARIO 4: Witness statements with conflicting accident directions
        {
            "claim_id": "CLM-2026-004",
            "title": "Intersection T-Bone with Contradictory Witness Statements",
            "scenario_type": "conflicting_witnesses",
            "status": "investigation_active",
            "priority": "high",
            "priority_score": 74.0,
            "claimant": {"name": "Karthik Subramanian", "phone": "+91 97654 32109", "email": "karthik.s@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-004", "registration": "TN-09-EF-3344", "vin": "MB1ZA61S00918234",
                "make": "Toyota", "model": "Innova Crysta", "year": 2021, "color": "Garnet Red", "body_type": "MPV"
            },
            "policy": {
                "policy_id": "POL-004", "policy_number": "POL-TOY-2025-9921",
                "holder": "Karthik Subramanian", "coverage_type": "Comprehensive",
                "start_date": "2025-05-20T00:00:00Z", "end_date": "2026-05-19T23:59:59Z",
                "deductible": 2000, "coverage_limit": 1900000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-14", "time": "16:40:00",
                "location": "Anna Salai - Mount Road Signal, Chennai",
                "accident_type": "Intersection Right-Angle T-Bone",
                "damage_estimate": 115000,
                "third_party": "Mahindra Thar (TN-07-QQ-9911)",
                "narrative": "I had a green signal and was moving straight North on Anna Salai. A red Thar approaching from the East ran a solid red light and rammed into my right front quarter."
            },
            "evidence_items": [
                {"id": "EVD-004-1", "name": "right_fender_tbone.jpg", "type": "image", "source": "Investigator Camera", "size": "3.9 MB", "hash": "3344mb1za61s00918234e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b", "notes": ["Direct right front wheel well and door intrusion", "Axle misalignment"]},
                {"id": "EVD-004-2", "name": "claimant_statement.pdf", "type": "statement", "source": "Driver Karthik", "size": "310 KB", "hash": "9921poltoy2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Claimant: 'I went straight on green. Thar crossed from East on red.'"]},
                {"id": "EVD-004-3", "name": "eyewitness_traffic_warden.pdf", "type": "statement", "source": "Traffic Warden M. Selvam", "size": "380 KB", "hash": "44917a22e84191a8c3e444b82d718a245582f6e729a73e4492b118a1a441e8b2", "notes": ["Warden states: 'The Innova took an abrupt free right turn without waiting for the green arrow filter, clipping the oncoming Thar that had right-of-way.'"]},
                {"id": "EVD-004-4", "name": "pedestrian_witness_b.pdf", "type": "statement", "source": "Eyewitness S. Ramesh", "size": "290 KB", "hash": "8b45f36e492161726a457d81a942a49281a17b8f9e11c84119b48c3b44b82d71", "notes": ["Pedestrian states: 'Both vehicles were driving fast attempting to beat the amber signal change.'"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-004-1",
                    "category": "Witness Divergence on Right of Way and Heading",
                    "severity": "High",
                    "sources_involved": ["EVD-004-2 (Claimant)", "EVD-004-3 (Traffic Warden)", "EVD-004-4 (Pedestrian)"],
                    "description": "Claimant asserts straight travel on green; official traffic warden asserts Claimant initiated an unauthorized right turn across oncoming traffic; bystander suggests amber race.",
                    "materiality": "Determines third-party recovery subrogation potential vs Own-Damage contributory fault.",
                    "alternative_explanations": ["Traffic signal green arrow filter was misread by claimant", "Warden observed another vehicle moments prior"],
                    "resolution_evidence": "Obtain automated Chennai Traffic Police ANPR/Smart City signal timing and camera sync."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-004-A",
                    "title": "Unauthorized Right Turn into Oncoming Path",
                    "support_level": "Supported by Official Witness",
                    "probability_score": 0.65,
                    "summary": "Claimant attempted right turn across traffic without dedicated green filter signal.",
                    "supporting_evidence": ["EVD-004-3", "EVD-004-1"],
                    "contradicting_evidence": ["EVD-004-2"],
                    "assumptions": ["Traffic warden positioned at island had clear view of turn"]
                },
                {
                    "hypothesis_id": "HYP-004-B",
                    "title": "Straight Transit with Third-Party Signal Violation",
                    "support_level": "Supported Solely by Claimant",
                    "probability_score": 0.35,
                    "summary": "Claimant went straight and third party breached signal.",
                    "supporting_evidence": ["EVD-004-2"],
                    "contradicting_evidence": ["EVD-004-3", "EVD-004-4"],
                    "assumptions": ["Third party accelerated into yellow phase"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent", "score": 85, "details": "45-degree angle of bumper impact aligns with right turn trajectory observed by warden."},
                "environmental_feasibility": {"status": "Verified", "score": 92, "details": "Daylight, dry asphalt, clear visibility."},
                "damage_consistency": {"status": "Aligned", "score": 88, "details": "Damage vector points to angled T-bone impact."},
                "repair_anomaly": {"status": "Normal", "score": 90, "details": "Toyota parts and labor costs within normal dealer tariff."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-004-1",
                    "action": "Request Chennai Smart City Junction CCTV & Signal Phase Log",
                    "priority": "Critical",
                    "uncertainty_addressed": "Resolves direct contradiction between claimant narrative and traffic warden testimony",
                    "expected_information_gain": 0.96,
                    "materiality": 0.92,
                    "reliability": 0.99,
                    "cost": 0.30,
                    "rank_score": 2.19,
                    "status": "sent",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 115000,
                "deductible": 2000,
                "depreciation_deduction": 0,
                "salvage_allowance": 4000,
                "indicative_payout": 109000,
                "currency": "INR",
                "policy_clause": "Comprehensive Section 1: OD claim payable subject to 50% recovery action against third party if signal breach confirmed."
            }
        },

        # SCENARIO 5: Incorrectly associated accident photographs
        {
            "claim_id": "CLM-2026-005",
            "title": "EXIF Temporal & Geolocation Mismatch on Submitted Evidence",
            "scenario_type": "metadata_mismatch",
            "status": "investigation_active",
            "priority": "high",
            "priority_score": 89.2,
            "claimant": {"name": "Vikram Sethi", "phone": "+91 94433 22110", "email": "vikram.sethi@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-005", "registration": "KA-01-MJ-7766", "vin": "KNAFX81A0P518294",
                "make": "Kia", "model": "Seltos HTX", "year": 2024, "color": "Imperial Blue", "body_type": "SUV"
            },
            "policy": {
                "policy_id": "POL-005", "policy_number": "POL-KIA-2025-3310",
                "holder": "Vikram Sethi", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-01-10T00:00:00Z", "end_date": "2026-01-09T23:59:59Z",
                "deductible": 1000, "coverage_limit": 1600000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-16", "time": "11:30:00",
                "location": "Hebbal Flyover, Bengaluru",
                "accident_type": "Guardrail Scrape",
                "damage_estimate": 48000,
                "third_party": "None",
                "narrative": "I grazed the highway divider barrier when dodging a stray dog on Hebbal flyover on Monday morning."
            },
            "evidence_items": [
                {"id": "EVD-005-1", "name": "kia_divider_scrape.jpg", "type": "image", "source": "Claimant Upload", "size": "4.8 MB", "hash": "7766knafx81a0p518294e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b", "notes": ["Left quarter panel scrape", "EXIF Date: 2025-12-14 15:22:10 (92 days prior)", "EXIF GPS: 19.0760° N, 72.8777° E (Mumbai)"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-005-1",
                    "category": "EXIF Digital Forensic Metadata Discrepancy",
                    "severity": "Critical",
                    "sources_involved": ["EVD-005-1 (Metadata Header)", "Claimant Notification"],
                    "description": "Original EXIF timestamp embedded in submitted photograph records capture date of 14-Dec-2025 (92 days before reported loss date) and GPS coordinates placing vehicle in Mumbai, while claim claims Bengaluru crash on 16-Mar-2026.",
                    "materiality": "Fundamental - Potential re-use of an older claim or photographic recycling.",
                    "alternative_explanations": ["Claimant accidentally uploaded an old photo from gallery instead of current crash", "Camera phone date/time was incorrectly set"],
                    "resolution_evidence": "Request live in-app camera capture of vehicle with today's newspaper or geostamp."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-005-A",
                    "title": "Erroneous Photo Gallery Selection by Claimant",
                    "support_level": "Under Clarification",
                    "probability_score": 0.50,
                    "summary": "Claimant selected wrong file from phone gallery containing prior incident in Mumbai.",
                    "supporting_evidence": [],
                    "contradicting_evidence": ["EVD-005-1"],
                    "assumptions": ["Claimant has genuine fresh damage on vehicle currently in Bengaluru"]
                },
                {
                    "hypothesis_id": "HYP-005-B",
                    "title": "Recycled Prior Loss Submission",
                    "support_level": "Supported by Metadata Evidence",
                    "probability_score": 0.50,
                    "summary": "Old loss photos from December are being resubmitted under active policy.",
                    "supporting_evidence": ["EVD-005-1"],
                    "contradicting_evidence": [],
                    "assumptions": ["Vehicle never had a March 16 crash"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Insufficient Information", "score": 40, "details": "Damage pattern consistent with barrier, but provenance in question."},
                "environmental_feasibility": {"status": "Unverified", "score": 30, "details": "Incident place/time mismatch prevents environmental correlation."},
                "damage_consistency": {"status": "Discrepant", "score": 35, "details": "Metadata invalidates direct evidentiary link to claimed March 16 event."},
                "repair_anomaly": {"status": "Pending", "score": 70, "details": "Bodyshop quote awaiting physical vehicle reinspection."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-005-1",
                    "action": "Request Live In-App Forensic Inspection Capture with Real-Time Geotag",
                    "priority": "Critical",
                    "uncertainty_addressed": "Instantly resolves whether submitted image was an accidental upload or intentional recycled photo",
                    "expected_information_gain": 0.99,
                    "materiality": 0.95,
                    "reliability": 0.99,
                    "cost": 0.05,
                    "rank_score": 6.20,
                    "status": "sent",
                    "responsible": "Claimant"
                }
            ],
            "settlement": {
                "eligible_repair": 0,
                "deductible": 1000,
                "depreciation_deduction": 0,
                "salvage_allowance": 0,
                "indicative_payout": 0,
                "currency": "INR",
                "policy_clause": "Investigation Hold: General Conditions Clause 6 - Claim processing suspended pending authenticated proof of loss date and location."
            }
        },

        # SCENARIO 6: Incomplete repair estimate
        {
            "claim_id": "CLM-2026-006",
            "title": "Unitemized Lump-Sum Repair Estimate Submitted",
            "scenario_type": "incomplete_estimate",
            "status": "awaiting_evidence",
            "priority": "medium",
            "priority_score": 52.0,
            "claimant": {"name": "Deepak Verma", "phone": "+91 93111 22334", "email": "deepak.v@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-006", "registration": "DL-04-CA-8899", "vin": "MA1TL21A0R819284",
                "make": "Mahindra", "model": "XUV700 AX7", "year": 2023, "color": "Midnight Black", "body_type": "SUV"
            },
            "policy": {
                "policy_id": "POL-006", "policy_number": "POL-MAH-2025-7720",
                "holder": "Deepak Verma", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-07-01T00:00:00Z", "end_date": "2026-06-30T23:59:59Z",
                "deductible": 2000, "coverage_limit": 2100000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-11", "time": "08:15:00",
                "location": "DND Flyway, Delhi-Noida",
                "accident_type": "Front Grille & Sensor Impact",
                "damage_estimate": 145000,
                "third_party": "None",
                "narrative": "Flew over debris on the highway, damaging the front bumper, lower grill, and adaptive cruise radar sensor."
            },
            "evidence_items": [
                {"id": "EVD-006-1", "name": "lump_sum_garage_bill.pdf", "type": "estimate", "source": "Local Multibrand Garage", "size": "620 KB", "hash": "8899ma1tl21a0r819284e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b", "notes": ["Lump sum quotation 'Front End Restoration - ₹1,45,000'", "No itemized parts list", "No OEM part numbers", "No paint/labor breakdown"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-006-1",
                    "category": "Regulatory Non-Compliance in Estimate Documentation",
                    "severity": "Medium",
                    "sources_involved": ["EVD-006-1 (Garage Estimate)"],
                    "description": "Repairer provided a single consolidated charge without segregating radar sensor unit (OEM ₹38,000), plastic grill, labor hours, or paint materials.",
                    "materiality": "High - Unable to audit legitimate replacement costs against benchmarks.",
                    "alternative_explanations": ["Garage standard intake format before detailed mechanical teardown"],
                    "resolution_evidence": "Request standard IRDAI Form 10 itemized estimate from repairer."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-006-A",
                    "title": "Legitimate Damage with Incomplete Garage Paperwork",
                    "support_level": "Awaiting Documentation",
                    "probability_score": 0.80,
                    "summary": "Radar sensor and bumper damage genuine, but workshop has not supplied transparent itemization.",
                    "supporting_evidence": ["EVD-006-1"],
                    "contradicting_evidence": [],
                    "assumptions": ["Workshop has manufacturer diagnostic scan of faulty radar"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent", "score": 82, "details": "Debris impact explains lower front fascia and radar damage."},
                "environmental_feasibility": {"status": "Verified", "score": 90, "details": "Clear morning conditions."},
                "damage_consistency": {"status": "Aligned", "score": 85, "details": "Lower center frontal zone damage corresponds to highway obstacle."},
                "repair_anomaly": {"status": "Anomaly Detected", "score": 25, "details": "Zero line-item transparency; composite bill cannot be audited."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-006-1",
                    "action": "Request Itemized Workshop Estimate with OEM Part Numbers and Labor Breakdown",
                    "priority": "High",
                    "uncertainty_addressed": "Enables algorithmic benchmarking of parts and labor against OEM tariff",
                    "expected_information_gain": 0.85,
                    "materiality": 0.80,
                    "reliability": 0.95,
                    "cost": 0.10,
                    "rank_score": 3.23,
                    "status": "sent",
                    "responsible": "Claimant"
                }
            ],
            "settlement": {
                "eligible_repair": 0,
                "deductible": 2000,
                "depreciation_deduction": 0,
                "salvage_allowance": 0,
                "indicative_payout": 0,
                "currency": "INR",
                "policy_clause": "Claims Procedures Rule 3.3: All estimates must be itemized into parts, labor, and paint consumables before assessment."
            }
        },

        # SCENARIO 7: Unusually high repair costs
        {
            "claim_id": "CLM-2026-007",
            "title": "Repair Cost Inflation on Electric Vehicle Headlamp Assembly",
            "scenario_type": "cost_inflation",
            "status": "investigation_active",
            "priority": "medium",
            "priority_score": 63.8,
            "claimant": {"name": "Sanjay Kapoor", "phone": "+91 98220 11223", "email": "sanjay.kapoor@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-007", "registration": "MH-12-PQ-4567", "vin": "MAT61201S00291823",
                "make": "Tata", "model": "Nexon EV Max", "year": 2023, "color": "Intensi-Teal", "body_type": "EV SUV"
            },
            "policy": {
                "policy_id": "POL-007", "policy_number": "POL-TAT-2025-5510",
                "holder": "Sanjay Kapoor", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-09-01T00:00:00Z", "end_date": "2026-08-31T23:59:59Z",
                "deductible": 1000, "coverage_limit": 1400000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-08", "time": "19:00:00",
                "location": "JM Road, Pune",
                "accident_type": "Low-Speed Corner Clip",
                "damage_estimate": 118000,
                "third_party": "Two-wheeler",
                "narrative": "Two-wheeler brushed against left front bumper and cracked the headlight lens in heavy market traffic."
            },
            "evidence_items": [
                {"id": "EVD-007-1", "name": "nexon_headlight_crack.jpg", "type": "image", "source": "Workshop Intake", "size": "3.1 MB", "hash": "4567mat61201s00291823e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b", "notes": ["Cracked polycarbonate outer lens", "Internal LED projector functioning", "Minor bumper scuff"]},
                {"id": "EVD-007-2", "name": "workshop_repair_quote.pdf", "type": "estimate", "source": "Elite Motor Works Pune", "size": "750 KB", "hash": "5510poltat2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["LED Headlamp assembly: ₹85,000", "Labor hours: 18.0 hours @ ₹1,200/hr = ₹21,600", "Paint charges: ₹11,400"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-007-1",
                    "category": "Price Gouging / Dynamic Cost Benchmark Deviation",
                    "severity": "Medium",
                    "sources_involved": ["EVD-007-2 (Estimate)", "Database Repair Benchmark (bmk-007)"],
                    "description": "Quoted headlamp assembly price of ₹85,000 is 220% higher than authorized Tata OEM list price of ₹26,500. Quoted labor of 18 hours exceeds benchmark replacement time of 1.5 hours by 1,100%.",
                    "materiality": "Material - ₹68,500 unjustified inflation.",
                    "alternative_explanations": ["Workshop quoted complete wiring harness assembly instead of individual headlamp", "Clerical error in bill entry"],
                    "resolution_evidence": "Cross-reference with Tata Motors Master Parts Price List."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-007-A",
                    "title": "Legitimate Claim with Inflated Bodyshop Billing",
                    "support_level": "Supported by Benchmarks",
                    "probability_score": 0.88,
                    "summary": "Incident is genuine but repairer is charging exorbitant parts and labor markups.",
                    "supporting_evidence": ["EVD-007-1", "EVD-007-2"],
                    "contradicting_evidence": [],
                    "assumptions": ["Damage was caused by two-wheeler as described"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent", "score": 90, "details": "Brushing impact from bike matches lens fracture."},
                "environmental_feasibility": {"status": "Verified", "score": 92, "details": "Pune urban traffic conditions verified."},
                "damage_consistency": {"status": "Aligned", "score": 92, "details": "Superficial corner damage consistent."},
                "repair_anomaly": {"status": "Anomaly Detected", "score": 28, "details": "Severe benchmark price deviation (+220% on part, +1,100% on labor)."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-007-1",
                    "action": "Issue Approved Tariff Adjustment to Authorized OEM Benchmark (₹39,500)",
                    "priority": "High",
                    "uncertainty_addressed": "Eliminates unjustified billing inflation while settling genuine loss",
                    "expected_information_gain": 0.90,
                    "materiality": 0.85,
                    "reliability": 0.98,
                    "cost": 0.05,
                    "rank_score": 5.00,
                    "status": "pending",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 39500,
                "deductible": 1000,
                "depreciation_deduction": 0,
                "salvage_allowance": 1200,
                "indicative_payout": 37300,
                "currency": "INR",
                "policy_clause": "Condition 5: The insurer's liability for parts shall not exceed the manufacturer's recommended retail price (MSRP) and prevailing authorized labor schedule."
            }
        },

        # SCENARIO 8: Accident date near a policy coverage change
        {
            "claim_id": "CLM-2026-008",
            "title": "Coverage Borderline Determination at Midnight Policy Transition",
            "scenario_type": "policy_timeline_transition",
            "status": "investigation_active",
            "priority": "medium",
            "priority_score": 58.0,
            "claimant": {"name": "Ananya Joshi", "phone": "+91 97111 88990", "email": "ananya.j@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-008", "registration": "MH-01-EE-6655", "vin": "WVWZZZ61S00718294",
                "make": "Volkswagen", "model": "Virtus Topline", "year": 2022, "color": "Wild Cherry Red", "body_type": "Sedan"
            },
            "policy": {
                "policy_id": "POL-008", "policy_number": "POL-VW-2025-1100",
                "holder": "Ananya Joshi", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-03-15T00:00:00Z", "end_date": "2026-03-14T23:59:59Z",
                "deductible": 1000, "coverage_limit": 1350000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-14", "time": "23:48:00",
                "location": "Bandra-Worli Sea Link Toll Plaza, Mumbai",
                "accident_type": "Toll Barrier Gate Strike",
                "damage_estimate": 42000,
                "third_party": "None",
                "narrative": "Toll arm malfunctioned and came down prematurely on my vehicle's windshield and hood at 23:48 on March 14."
            },
            "evidence_items": [
                {"id": "EVD-008-1", "name": "toll_plaza_slip.pdf", "type": "document", "source": "MEP Toll Authority", "size": "420 KB", "hash": "6655wvwzzz61s00718294e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b", "notes": ["Toll transaction timestamp: 14-Mar-2026 23:47:52", "Lane 4 Northbound"]},
                {"id": "EVD-008-2", "name": "policy_v1_terms.pdf", "type": "document", "source": "Policy Repository", "size": "1.2 MB", "hash": "1100polvw2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Policy V1 with Zero-Depreciation Add-on expires March 14, 2026 at 23:59:59"]},
                {"id": "EVD-008-3", "name": "policy_v2_renewal.pdf", "type": "document", "source": "Renewal System", "size": "1.1 MB", "hash": "2200polvw2026e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Renewed Policy V2 starts March 15, 2026 at 00:00:00 (Standard policy with ₹5,000 deductible and NO zero-depreciation waiver)"]}
            ],
            "contradictions": [],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-008-A",
                    "title": "Loss Incurred Under Policy Version 1 (Zero-Dep Valid)",
                    "support_level": "Forensically Confirmed",
                    "probability_score": 0.98,
                    "summary": "Toll receipt timestamp of 23:47:52 proves loss occurred 12 minutes before expiration of Policy Version 1.",
                    "supporting_evidence": ["EVD-008-1", "EVD-008-2"],
                    "contradicting_evidence": [],
                    "assumptions": ["Toll plaza server clock synchronized with NTP server"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent", "score": 94, "details": "Boom barrier descent accounts for hood scratch and windshield glass stress line."},
                "environmental_feasibility": {"status": "Verified", "score": 95, "details": "Clear weather, sea link transit logged."},
                "damage_consistency": {"status": "Aligned", "score": 92, "details": "Linear overhead impact matches automated gate arm."},
                "repair_anomaly": {"status": "Normal", "score": 90, "details": "Windshield and hood paint costs align with Volkswagen tariff."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-008-1",
                    "action": "Verify Sea Link Fastag Electronic Toll Server NTP Timestamp",
                    "priority": "Medium",
                    "uncertainty_addressed": "Conclusively certifies loss timing within 12-minute window of policy transition",
                    "expected_information_gain": 0.60,
                    "materiality": 0.70,
                    "reliability": 0.99,
                    "cost": 0.05,
                    "rank_score": 2.77,
                    "status": "completed",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 42000,
                "deductible": 1000,
                "depreciation_deduction": 0,
                "salvage_allowance": 800,
                "indicative_payout": 40200,
                "currency": "INR",
                "policy_clause": "Deterministic Decision: Incident at 23:48 falls squarely within Policy V1 period. Full Zero-Depreciation benefits apply (saving policyholder ₹12,600 compared to V2)."
            }
        },

        # SCENARIO 9: Environmental conditions requiring verification
        {
            "claim_id": "CLM-2026-009",
            "title": "Hydroplaning Claim Inconsistent with Meteorological Records",
            "scenario_type": "environmental_discrepancy",
            "status": "investigation_active",
            "priority": "high",
            "priority_score": 76.5,
            "claimant": {"name": "Rohan Deshmukh", "phone": "+91 98450 67890", "email": "rohan.d@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-009", "registration": "KA-04-MN-1122", "vin": "TMBJF81S003819284",
                "make": "Skoda", "model": "Slavia Style", "year": 2022, "color": "Crystal Blue", "body_type": "Sedan"
            },
            "policy": {
                "policy_id": "POL-009", "policy_number": "POL-SKO-2025-6677",
                "holder": "Rohan Deshmukh", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-06-15T00:00:00Z", "end_date": "2026-06-14T23:59:59Z",
                "deductible": 1500, "coverage_limit": 1500000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-13", "time": "15:30:00",
                "location": "Nice Road expressway, Hosur Road exit, Bengaluru",
                "accident_type": "Single Vehicle Skid & Spin-out",
                "damage_estimate": 74000,
                "third_party": "None",
                "narrative": "A torrential cloudburst flooded the highway within minutes. My tires lost traction on deep standing water, causing severe hydroplaning into the concrete ditch."
            },
            "evidence_items": [
                {"id": "EVD-009-1", "name": "underbody_rocker_dent.jpg", "type": "image", "source": "Field Inspection", "size": "3.6 MB", "hash": "1122tmbjf81s003819284e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b", "notes": ["Bent lower control arm", "Crushed rocker panel right", "Ditch impact scratches"]},
                {"id": "EVD-009-2", "name": "imd_weather_station_data.pdf", "type": "document", "source": "India Meteorological Dept / OpenWeather API", "size": "510 KB", "hash": "6677polsko2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Bengaluru South NICE corridor: 0.0mm rainfall recorded between 12:00-18:00 on 13-Mar-2026", "Temperature: 33.8°C", "Relative Humidity: 38%", "Road surface: Dry"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-009-1",
                    "category": "Environmental & Meteorological Contradiction",
                    "severity": "High",
                    "sources_involved": ["EVD-009-2 (IMD Official Station)", "Claimant Narrative"],
                    "description": "Claimant asserts sudden torrential cloudburst and extensive road flooding induced loss of control. Official regional radar and weather station records 0.0mm rainfall and clear 33.8°C dry conditions throughout the day.",
                    "materiality": "Material - Calls into question stated speed, driver attention, or actual mechanism of ditch impact.",
                    "alternative_explanations": ["Local water tanker spill on highway", "Driver fell asleep or was distracted and fabricated rain justification"],
                    "resolution_evidence": "Retrieve electronic stability control (ESC) sensor logs from vehicle ECU."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-009-A",
                    "title": "Driver Inattention / Excessive Speed in Dry Conditions",
                    "support_level": "Supported by Weather Telemetry",
                    "probability_score": 0.75,
                    "summary": "Vehicle left roadway due to speed or distraction; rain narrative used to deflect personal liability.",
                    "supporting_evidence": ["EVD-009-2"],
                    "contradicting_evidence": ["Claimant Narrative"],
                    "assumptions": ["Ditch collision is physical reality but cause is driver error"]
                },
                {
                    "hypothesis_id": "HYP-009-B",
                    "title": "Isolated Localized Liquid Spill (Non-Rain)",
                    "support_level": "Unverified Alternative",
                    "probability_score": 0.25,
                    "summary": "Industrial tanker or commercial spill caused localized traction loss.",
                    "supporting_evidence": [],
                    "contradicting_evidence": ["EVD-009-2"],
                    "assumptions": ["Spill evaporated before highway patrol inspection"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent", "score": 85, "details": "Control arm deflection matches high-velocity curb impact."},
                "environmental_feasibility": {"status": "Unverified / Contradictory", "score": 20, "details": "Meteorological records definitively refute rain/hydroplaning assertion."},
                "damage_consistency": {"status": "Aligned", "score": 80, "details": "Underbody trauma consistent with off-road departure."},
                "repair_anomaly": {"status": "Normal", "score": 88, "details": "Suspension parts priced according to Skoda catalog."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-009-1",
                    "action": "Download Skoda On-Board Airbag Control Unit (ACU) Yaw Rate & Speed Data",
                    "priority": "High",
                    "uncertainty_addressed": "Ascertains actual pre-crash vehicle velocity and steering angle prior to ditch impact",
                    "expected_information_gain": 0.94,
                    "materiality": 0.88,
                    "reliability": 0.99,
                    "cost": 0.25,
                    "rank_score": 2.36,
                    "status": "pending",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 74000,
                "deductible": 1500,
                "depreciation_deduction": 0,
                "salvage_allowance": 2500,
                "indicative_payout": 70000,
                "currency": "INR",
                "policy_clause": "Coverage Note: While environmental cause is inconsistent, Comprehensive Own-Damage covers single-vehicle accidental ditch strikes irrespective of driver negligence, provided no intoxicating substances were involved."
            }
        },

        # SCENARIO 10: Insufficient evidence to distinguish multiple accident explanations
        {
            "claim_id": "CLM-2026-010",
            "title": "Three-Vehicle Highway Chain Collision Sequence Ambiguity",
            "scenario_type": "multi_hypothesis_ambiguity",
            "status": "investigation_active",
            "priority": "urgent",
            "priority_score": 91.5,
            "claimant": {"name": "Meera Nambiar", "phone": "+91 96543 21098", "email": "meera.n@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-010", "registration": "KA-51-MD-9001", "vin": "MA1ZE81S009182341",
                "make": "MG", "model": "Hector Sharp Pro", "year": 2023, "color": "Starry Black", "body_type": "SUV"
            },
            "policy": {
                "policy_id": "POL-010", "policy_number": "POL-MG-2025-4499",
                "holder": "Meera Nambiar", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-10-01T00:00:00Z", "end_date": "2026-09-30T23:59:59Z",
                "deductible": 2000, "coverage_limit": 1850000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-09", "time": "09:30:00",
                "location": "Electronic City Elevated Expressway km 8, Bengaluru",
                "accident_type": "3-Vehicle Accordion Pileup",
                "damage_estimate": 165000,
                "third_party": "Lead Vehicle: Fortuner (KA-01-XX-1111), Trailing Vehicle: Bus (KA-57-F-9988)",
                "narrative": "Traffic stopped suddenly. I came to a complete, safe halt 2 meters behind the Fortuner. Seconds later, a trailing private bus rammed into my rear at speed, violently thrusting my vehicle forward into the rear of the Fortuner."
            },
            "evidence_items": [
                {"id": "EVD-010-1", "name": "front_and_rear_crush.jpg", "type": "image", "source": "Expressway Patrol", "size": "4.4 MB", "hash": "9001ma1ze81s009182341e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b", "notes": ["Both front grille/radiator and rear tailgate/chassis crushed", "Accordion damage pattern"]},
                {"id": "EVD-010-2", "name": "lead_driver_fortuner_statement.pdf", "type": "statement", "source": "Driver Alok Roy", "size": "360 KB", "hash": "4499polmg2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Lead driver statements: 'I felt two distinct shocks in rapid succession: first a hard bump, then a few seconds later a much violent jolt that pushed me forward.'"]},
                {"id": "EVD-010-3", "name": "bus_driver_statement.pdf", "type": "statement", "source": "Bus Driver Ramesh", "size": "320 KB", "hash": "7788polbus2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Bus driver claims: 'The MG Hector had already crashed into the Fortuner before I arrived; I tried to swerve but grazed their rear.'"]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-010-1",
                    "category": "Impact Sequence Contradiction Across 3 Drivers",
                    "severity": "Critical",
                    "sources_involved": ["EVD-010-1 (Damage)", "EVD-010-2 (Lead Driver)", "EVD-010-3 (Bus Driver)", "Claimant Narrative"],
                    "description": "Claimant insists she was pushed into the front car solely by the bus. Lead Fortuner driver reports feeling two distinct impacts, supporting the bus driver's claim that the MG struck the Fortuner first before the bus arrived.",
                    "materiality": "Fundamental - Decides 100% liability subrogation against bus company vs Claimant front-impact fault.",
                    "alternative_explanations": ["First shock felt by lead driver was the initial bus impact transferring through, second shock was secondary recoil", "Claimant had already struck lead car first"],
                    "resolution_evidence": "Extract EDR (Event Data Recorder) dual-event crash pulse records from MG Hector."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-010-A",
                    "title": "H1: Sandwiched from Behind (Claimant Innocent)",
                    "support_level": "Supported by Claimant Account",
                    "probability_score": 0.45,
                    "summary": "Claimant halted in time; bus impact initiated whole sequence, projecting Hector into Fortuner.",
                    "supporting_evidence": ["EVD-010-1", "Claimant Narrative"],
                    "contradicting_evidence": ["EVD-010-2 (Lead Driver mentions two shocks)"],
                    "assumptions": ["Lead driver felt primary impact and subsequent recoil"]
                },
                {
                    "hypothesis_id": "HYP-010-B",
                    "title": "H2: Claimant Rear-Ended Lead Car First, Then Struck by Bus",
                    "support_level": "Supported by Lead Driver Testimony",
                    "probability_score": 0.55,
                    "summary": "Claimant failed to stop, crashed into Fortuner (1st impact), then bus impacted Hector from behind (2nd impact).",
                    "supporting_evidence": ["EVD-010-2", "EVD-010-3"],
                    "contradicting_evidence": ["Claimant Narrative"],
                    "assumptions": ["Dual impact sensation corresponds to two independent collisions"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Equally Plausible Across H1 & H2", "score": 50, "details": "Both collision sequences physically account for dual crush zones."},
                "environmental_feasibility": {"status": "Verified", "score": 90, "details": "Normal morning rush-hour conditions."},
                "damage_consistency": {"status": "Ambiguous Kinetic Vector", "score": 45, "details": "Front radiator frame displays both primary crush and secondary intrusion."},
                "repair_anomaly": {"status": "Normal", "score": 85, "details": "Structural quote corresponds to heavy front-rear restoration."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-010-1",
                    "action": "Extract Bosch EDR Crash Pulse Telematics from MG Hector Airbag Control Module",
                    "priority": "Critical",
                    "uncertainty_addressed": "Decisively reveals exact millisecond timestamp delta between front sensor delta-V and rear sensor delta-V",
                    "expected_information_gain": 0.99,
                    "materiality": 0.98,
                    "reliability": 0.99,
                    "cost": 0.35,
                    "rank_score": 2.76,
                    "status": "sent",
                    "responsible": "Investigator"
                },
                {
                    "rec_id": "REC-010-2",
                    "action": "Subpoena Electronic City Tollway Surveillance Camera C-8",
                    "priority": "High",
                    "uncertainty_addressed": "Provides video timeline of approaching bus and spacing between Fortuner and Hector",
                    "expected_information_gain": 0.95,
                    "materiality": 0.90,
                    "reliability": 0.95,
                    "cost": 0.40,
                    "rank_score": 1.62,
                    "status": "pending",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 165000,
                "deductible": 2000,
                "depreciation_deduction": 0,
                "salvage_allowance": 6000,
                "indicative_payout": 157000,
                "currency": "INR",
                "policy_clause": "Full Own-Damage indemnity approved. Final subrogation apportionment against trailing bus insurer reserved pending EDR findings."
            }
        },

        # SCENARIO 11: High-Impact Loss Over 5 Lakhs Threshold (Guardrail Mandate)
        {
            "claim_id": "CLM-2026-011",
            "title": "High-Impact BMW Structural Collision (> ₹5 Lakhs Guardrail Active)",
            "scenario_type": "high_impact_over_5l",
            "status": "escalated_to_siu",
            "priority": "urgent",
            "priority_score": 94.2,
            "claimant": {"name": "Siddharth Singhania", "phone": "+91 98111 55667", "email": "siddharth.s@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-011", "registration": "DL-01-EE-0007", "vin": "WBA33AY08P0091823",
                "make": "BMW", "model": "330i M Sport", "year": 2023, "color": "Portimao Blue", "body_type": "Sedan"
            },
            "policy": {
                "policy_id": "POL-011", "policy_number": "POL-BMW-2025-0077",
                "holder": "Siddharth Singhania", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-05-01T00:00:00Z", "end_date": "2026-04-30T23:59:59Z",
                "deductible": 5000, "coverage_limit": 4800000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-18", "time": "22:15:00",
                "location": "Golf Course Road Underpass, Gurugram",
                "accident_type": "High-Speed Guardrail Barrier Strike",
                "damage_estimate": 780000,
                "third_party": "None",
                "narrative": "Swerved to avoid an unlit obstacle in the underpass; struck the galvanized crash barrier at 65 km/h, crumpling front right suspension, steering rack, and adaptive laser headlamp."
            },
            "evidence_items": [
                {"id": "EVD-011-1", "name": "bmw_suspension_crush.jpg", "type": "image", "source": "BMW Authorized Service", "size": "4.8 MB", "hash": "0007wba33ay08pe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Bent steering knuckle", "Cracked front subframe", "Shattered RHS Laser Headlamp (OEM ₹1.95L)"]},
                {"id": "EVD-011-2", "name": "bmw_bodyshop_quote.pdf", "type": "estimate", "source": "BMW Bird Automotive", "size": "1.4 MB", "hash": "7700polbmw2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Parts: ₹5,80,000", "Labor: ₹1,45,000", "Taxes: ₹55,000", "Total: ₹7,80,000"]}
            ],
            "contradictions": [],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-011-A",
                    "title": "High-Velocity Underpass Barrier Collision",
                    "support_level": "Verified Mechanical Trauma",
                    "probability_score": 0.95,
                    "summary": "Subframe shear angles and suspension deformation conform to 60-70 km/h kinetic impact with steel barrier.",
                    "supporting_evidence": ["EVD-011-1", "EVD-011-2"],
                    "contradicting_evidence": [],
                    "assumptions": ["Electronic stability control logged lateral acceleration event"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent with Underpass Barrier", "score": 92, "details": "Suspension deformation kinetics match 65 km/h barrier deflection."},
                "environmental_feasibility": {"status": "Verified", "score": 90, "details": "Dry road surface, lighted underpass."},
                "damage_consistency": {"status": "Aligned", "score": 94, "details": "Impact concentrated on front-right mechanical corner."},
                "repair_anomaly": {"status": "High-Impact Exposure", "score": 85, "details": "Quote of ₹7,80,000 conforms to BMW authorized pricing but triggers SIU executive threshold."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-011-1",
                    "action": "Mandatory Executive Sign-Off (Chief Compliance Officer Authorization)",
                    "priority": "Critical",
                    "uncertainty_addressed": "Enforces IRDAI Guardrail: Losses over ₹5,00,000 strictly prohibit unilateral investigator settlement",
                    "expected_information_gain": 0.99,
                    "materiality": 0.99,
                    "reliability": 0.99,
                    "cost": 0.05,
                    "rank_score": 6.53,
                    "status": "sent",
                    "responsible": "Chief Compliance Officer",
                    "hypotheses_distinguished": ["Executive SIU Approval"]
                }
            ],
            "settlement": {
                "eligible_repair": 780000,
                "deductible": 5000,
                "depreciation_deduction": 0,
                "salvage_allowance": 18000,
                "indicative_payout": 757000,
                "currency": "INR",
                "policy_clause": "GUARDRAIL ACTIVE: High-Impact Loss Governance Rule 14.3. Claim exceeds ₹5,00,000 threshold. Settlement requires Chief Compliance Officer (Admin) executive sign-off."
            }
        },

        # SCENARIO 12: High-Impact Catastrophic Frame Rollover (> ₹5 Lakhs Guardrail)
        {
            "claim_id": "CLM-2026-012",
            "title": "Mercedes-Benz E-Class Rollover Total Loss (> ₹5 Lakhs Guardrail Active)",
            "scenario_type": "high_impact_over_5l",
            "status": "decision_pending",
            "priority": "urgent",
            "priority_score": 98.5,
            "claimant": {"name": "Gaurav Singhal", "phone": "+91 99220 88991", "email": "gaurav.s@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-012", "registration": "MH-01-BK-1100", "vin": "WDD21301S00819284",
                "make": "Mercedes-Benz", "model": "E-Class E220d", "year": 2023, "color": "Obsidian Black", "body_type": "Sedan"
            },
            "policy": {
                "policy_id": "POL-012", "policy_number": "POL-MB-2025-9988",
                "holder": "Gaurav Singhal", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-08-01T00:00:00Z", "end_date": "2026-07-31T23:59:59Z",
                "deductible": 5000, "coverage_limit": 6200000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-12", "time": "02:30:00",
                "location": "Mumbai-Pune Expressway km 42",
                "accident_type": "Highway Rollover & Multi-Panel Crush",
                "damage_estimate": 1450000,
                "third_party": "None",
                "narrative": "Tire blowout at 95 km/h caused vehicle to spin across median embankment and roll onto its roof and right side."
            },
            "evidence_items": [
                {"id": "EVD-012-1", "name": "mercedes_roof_crush.jpg", "type": "image", "source": "Highway Patrol", "size": "4.9 MB", "hash": "1100wdd21301se3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["A-Pillar deformation", "Roof crush", "Curtain airbags deployed", "Chassis twist"]},
                {"id": "EVD-012-2", "name": "mercedes_structural_survey.pdf", "type": "estimate", "source": "Mercedes-Benz Landmark", "size": "1.8 MB", "hash": "8899polmb2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Loss assessment: ₹14,50,000", "Exceeds 75% CTL threshold recommendation"]}
            ],
            "contradictions": [],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-012-A",
                    "title": "Catastrophic High-Speed Embankment Rollover",
                    "support_level": "Forensically Corroborated",
                    "probability_score": 0.98,
                    "summary": "Full cabin structural compromise and all airbag squibs fired consistent with embankment rollover.",
                    "supporting_evidence": ["EVD-012-1", "EVD-012-2"],
                    "contradicting_evidence": [],
                    "assumptions": ["Tire tread delamination initiated loss of control"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Consistent with Embankment Rollover", "score": 96, "details": "Omni-directional roof and pillar stress fractures indicate 360-degree roll."},
                "environmental_feasibility": {"status": "Verified", "score": 92, "details": "Expressway conditions verified."},
                "damage_consistency": {"status": "Aligned", "score": 95, "details": "Severe structural deformation."},
                "repair_anomaly": {"status": "Constructive Total Loss (> ₹5L Guardrail)", "score": 88, "details": "Loss exposure of ₹14.5L strictly requires Chief Compliance Officer authorization."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-012-1",
                    "action": "Executive Sign-Off & Salvage Tender Approval (Chief Compliance Officer)",
                    "priority": "Critical",
                    "uncertainty_addressed": "Enforces IRDAI Guardrail: Claims > ₹5L require Top Insurance Executive authorization",
                    "expected_information_gain": 0.99,
                    "materiality": 0.99,
                    "reliability": 0.99,
                    "cost": 0.05,
                    "rank_score": 6.53,
                    "status": "pending",
                    "responsible": "Chief Compliance Officer"
                }
            ],
            "settlement": {
                "eligible_repair": 1450000,
                "deductible": 5000,
                "depreciation_deduction": 0,
                "salvage_allowance": 250000,
                "indicative_payout": 1195000,
                "currency": "INR",
                "policy_clause": "GUARDRAIL ACTIVE: High-Impact Loss Governance Rule 14.3. Claim exceeds ₹5,00,000. Verification by Chief Compliance Officer (Admin) mandatory."
            }
        },

        # SCENARIO 13: Fresh Uninvestigated Dossier (Pending Initial AI Intake)
        {
            "claim_id": "CLM-2026-013",
            "title": "Fresh Intake: Parking Scrape on Rear Quarter (Uninvestigated)",
            "scenario_type": "uninvestigated_intake",
            "status": "intake_pending",
            "priority": "low",
            "priority_score": 18.0,
            "claimant": {"name": "Sneha Nair", "phone": "+91 97444 33221", "email": "sneha.nair@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-013", "registration": "KA-03-MM-5511", "vin": "MALB351SLPM009182",
                "make": "Hyundai", "model": "i20 Asta", "year": 2023, "color": "Fiery Red", "body_type": "Hatchback"
            },
            "policy": {
                "policy_id": "POL-013", "policy_number": "POL-HYU-2025-1199",
                "holder": "Sneha Nair", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-11-01T00:00:00Z", "end_date": "2026-10-31T23:59:59Z",
                "deductible": 1000, "coverage_limit": 850000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-20", "time": "12:10:00",
                "location": "Koramangala 5th Block, Bengaluru",
                "accident_type": "Parking Lot Scuff",
                "damage_estimate": 18000,
                "third_party": "None",
                "narrative": "Discovered minor scratch and dent on rear left quarter panel after parking for 2 hours outside restaurant."
            },
            "evidence_items": [
                {"id": "EVD-013-1", "name": "i20_rear_scratch.jpg", "type": "image", "source": "Claimant Smartphone Upload", "size": "2.4 MB", "hash": "5511malb351se3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Superficial clearcoat scratch", "Awaiting full SIU inference"]}
            ],
            "contradictions": [],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-013-A",
                    "title": "Low-Speed Parking Pillar Contact",
                    "support_level": "Preliminary Intake Pending",
                    "probability_score": 0.85,
                    "summary": "Dossier newly submitted; awaiting full computer vision analysis and bodyshop estimate verification.",
                    "supporting_evidence": ["EVD-013-1"],
                    "contradicting_evidence": [],
                    "assumptions": ["Contact occurred during parking maneuver"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Pending Investigation", "score": 85, "details": "Fresh submission awaiting initial surveyor inspection."},
                "environmental_feasibility": {"status": "Pending", "score": 85, "details": "Daylight parking lot scuff."},
                "damage_consistency": {"status": "Pending", "score": 85, "details": "Superficial clearcoat scrape."},
                "repair_anomaly": {"status": "Pending Estimate", "score": 85, "details": "Awaiting certified garage estimate."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-013-1",
                    "action": "Request Authorized Bodyshop Repair Estimate",
                    "priority": "Medium",
                    "uncertainty_addressed": "Establish baseline parts and refinish quotation",
                    "expected_information_gain": 0.70,
                    "materiality": 0.40,
                    "reliability": 0.90,
                    "cost": 0.10,
                    "rank_score": 1.26,
                    "status": "pending",
                    "responsible": "Claimant"
                }
            ],
            "settlement": {
                "eligible_repair": 18000,
                "deductible": 1000,
                "depreciation_deduction": 0,
                "salvage_allowance": 0,
                "indicative_payout": 17000,
                "currency": "INR",
                "policy_clause": "Standard Own-Damage section applies pending verification of final garage invoice."
            }
        },

        # SCENARIO 14: Fresh Commercial Fleet Intake (Uninvestigated)
        {
            "claim_id": "CLM-2026-014",
            "title": "Fresh Intake: Commercial Fleet Loading Dock Dent (Uninvestigated)",
            "scenario_type": "uninvestigated_intake",
            "status": "intake_pending",
            "priority": "medium",
            "priority_score": 38.0,
            "claimant": {"name": "Balaji Logistics", "phone": "+91 94440 12345", "email": "fleet@balajilogistics.com"},
            "vehicle": {
                "vehicle_id": "VEH-014", "registration": "KA-53-B-7788", "vin": "MAT37201S0091823",
                "make": "Tata", "model": "Ace Gold", "year": 2022, "color": "Arctic White", "body_type": "Mini Truck"
            },
            "policy": {
                "policy_id": "POL-014", "policy_number": "POL-TAT-2025-3390",
                "holder": "Balaji Logistics Pvt Ltd", "coverage_type": "Commercial Comprehensive",
                "start_date": "2025-06-01T00:00:00Z", "end_date": "2026-05-31T23:59:59Z",
                "deductible": 2500, "coverage_limit": 420000, "depreciation_waiver": False
            },
            "incident": {
                "date": "2026-03-21", "time": "07:45:00",
                "location": "APMC Yard Loading Bay 3, Yeshwanthpur",
                "accident_type": "Loading Bay Reversing Contact",
                "damage_estimate": 35000,
                "third_party": "None",
                "narrative": "Driver was reversing into warehouse dock; rear tailgate impacted concrete loading ramp edge."
            },
            "evidence_items": [
                {"id": "EVD-014-1", "name": "ace_tailgate_dent.jpg", "type": "image", "source": "Fleet Manager Upload", "size": "2.9 MB", "hash": "7788mat37201se3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Tailgate sheet metal depression", "Uninvestigated intake"]}
            ],
            "contradictions": [],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-014-A",
                    "title": "Low-Speed Loading Dock Impact",
                    "support_level": "Preliminary Intake Pending",
                    "probability_score": 0.88,
                    "summary": "Initial notification logged; awaiting driver trip sheet and formal repair quotation.",
                    "supporting_evidence": ["EVD-014-1"],
                    "contradicting_evidence": [],
                    "assumptions": ["Loading bay ramp height aligns with tailgate hinge"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Pending Investigation", "score": 80, "details": "Awaiting measurement of warehouse ramp height."},
                "environmental_feasibility": {"status": "Pending", "score": 90, "details": "Commercial yard operation."},
                "damage_consistency": {"status": "Pending", "score": 80, "details": "Horizontal tailgate dent."},
                "repair_anomaly": {"status": "Pending", "score": 80, "details": "Estimate pending surveyor physical audit."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-014-1",
                    "action": "Request Driver Daily Logbook & Loading Bay Ramp Alignment Photo",
                    "priority": "Medium",
                    "uncertainty_addressed": "Corroborate contact geometry against loading dock ramp",
                    "expected_information_gain": 0.75,
                    "materiality": 0.60,
                    "reliability": 0.90,
                    "cost": 0.10,
                    "rank_score": 2.02,
                    "status": "pending",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 35000,
                "deductible": 2500,
                "depreciation_deduction": 5000,
                "salvage_allowance": 1000,
                "indicative_payout": 26500,
                "currency": "INR",
                "policy_clause": "Commercial Vehicle Package Policy Section 1: Standard depreciation rules apply."
            }
        },

        # SCENARIO 15: Repudiated / Rejected Claim Under Policy Exclusion
        {
            "claim_id": "CLM-2026-015",
            "title": "Repudiated Claim: Driver License Breach Confirmed via Parivahan RTO",
            "scenario_type": "repudiated_exclusion",
            "status": "claim_rejected",
            "priority": "high",
            "priority_score": 88.0,
            "claimant": {"name": "Karan Malhotra", "phone": "+91 98333 44556", "email": "karan.m@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-015", "registration": "MH-04-DX-9090", "vin": "MA3FB71S00918234",
                "make": "Honda", "model": "Civic ZX", "year": 2021, "color": "Radiant Red", "body_type": "Sedan"
            },
            "policy": {
                "policy_id": "POL-015", "policy_number": "POL-HND-2025-9090",
                "holder": "Karan Malhotra", "coverage_type": "Comprehensive",
                "start_date": "2025-04-15T00:00:00Z", "end_date": "2026-04-14T23:59:59Z",
                "deductible": 2000, "coverage_limit": 1400000, "depreciation_waiver": False
            },
            "incident": {
                "date": "2026-03-05", "time": "23:40:00",
                "location": "Thane Ghodbunder Road, Mumbai",
                "accident_type": "Curb Impact & Wheel Rim Shatter",
                "damage_estimate": 120000,
                "third_party": "None",
                "narrative": "Car hit a raised concrete median curb in rain. Front alloy wheel shattered and steering arm snapped."
            },
            "evidence_items": [
                {"id": "EVD-015-1", "name": "civic_wheel_fracture.jpg", "type": "image", "source": "Investigator Camera", "size": "3.8 MB", "hash": "9090ma3fb71se3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Shattered 17-inch alloy rim", "Bent tie-rod"]},
                {"id": "EVD-015-2", "name": "parivahan_dl_verification.pdf", "type": "document", "source": "MoRTH Parivahan Portal", "size": "450 KB", "hash": "9090polhnd2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Official DL verification for driver named in police report: Driver License expired 14 months prior; no valid renewal."]}
            ],
            "contradictions": [
                {
                    "conflict_id": "CONF-015-1",
                    "category": "Statutory Policy Exclusion - Unlicensed Operation",
                    "severity": "Critical",
                    "sources_involved": ["EVD-015-2 (Parivahan RTO Extract)", "Policy Driver Clause"],
                    "description": "Government RTO registry establishes driver was operating vehicle on an expired license without valid driving entitlement at the time of loss.",
                    "materiality": "Fundamental - Total repudiation under statutory driver clause.",
                    "alternative_explanations": ["Clerical renewal pending at RTO"],
                    "resolution_evidence": "Confirmed via Parivahan digital API; repudiation notice issued."
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-015-A",
                    "title": "Breach of Fundamental Driver Clause",
                    "support_level": "Conclusively Established",
                    "probability_score": 0.99,
                    "summary": "Vehicle was driven by person without a valid driving license, fully excluding insurer liability under Section 3.",
                    "supporting_evidence": ["EVD-015-2"],
                    "contradicting_evidence": [],
                    "assumptions": ["RTO database record is authoritative"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Physically Consistent", "score": 90, "details": "Curb impact mechanically explains alloy rim fracture."},
                "environmental_feasibility": {"status": "Verified", "score": 88, "details": "Wet curb."},
                "damage_consistency": {"status": "Aligned", "score": 90, "details": "Rim fracture consistent."},
                "repair_anomaly": {"status": "Repudiation Mandated", "score": 10, "details": "Claim excluded from payment under Driver Clause 3.B."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-015-1",
                    "action": "Issue Formal Notice of Repudiation Under Driver Clause 3.B",
                    "priority": "High",
                    "uncertainty_addressed": "Concludes case with statutory repudiation declaration",
                    "expected_information_gain": 0.99,
                    "materiality": 0.99,
                    "reliability": 0.99,
                    "cost": 0.05,
                    "rank_score": 6.53,
                    "status": "completed",
                    "responsible": "Investigator"
                }
            ],
            "settlement": {
                "eligible_repair": 0,
                "deductible": 2000,
                "depreciation_deduction": 0,
                "salvage_allowance": 0,
                "indicative_payout": 0,
                "currency": "INR",
                "policy_clause": "REPUDIATED: General Exceptions Clause 3: The company shall not be liable for any accidental loss whilst vehicle is driven by any person not holding an effective driving licence."
            }
        },

        # SCENARIO 16: High-Impact Loss Cleared with Executive Authorization
        {
            "claim_id": "CLM-2026-016",
            "title": "Audi Q5 Highway Barrier Clip (> ₹5 Lakhs Guardrail - Executive Authorized)",
            "scenario_type": "high_impact_over_5l",
            "status": "investigation_completed",
            "priority": "high",
            "priority_score": 68.0,
            "claimant": {"name": "Radhika Merchant", "phone": "+91 98200 77112", "email": "radhika.m@example.com"},
            "vehicle": {
                "vehicle_id": "VEH-016", "registration": "MH-02-FF-8800", "vin": "WAUZZZFY0P0091823",
                "make": "Audi", "model": "Q5 Technology", "year": 2023, "color": "Navarra Blue", "body_type": "SUV"
            },
            "policy": {
                "policy_id": "POL-016", "policy_number": "POL-AUD-2025-8800",
                "holder": "Radhika Merchant", "coverage_type": "Comprehensive Zero-Dep",
                "start_date": "2025-07-01T00:00:00Z", "end_date": "2026-06-30T23:59:59Z",
                "deductible": 5000, "coverage_limit": 5200000, "depreciation_waiver": True
            },
            "incident": {
                "date": "2026-03-01", "time": "17:30:00",
                "location": "Eastern Freeway Exit, Mumbai",
                "accident_type": "Corner Barrier Clip",
                "damage_estimate": 650000,
                "third_party": "None",
                "narrative": "Exit ramp barrier grazed the front-left Matrix LED headlight, radar sensor, and carbon bumper valence."
            },
            "evidence_items": [
                {"id": "EVD-016-1", "name": "audi_matrix_headlamp.jpg", "type": "image", "source": "Audi South Mumbai", "size": "4.2 MB", "hash": "8800wauzzzfye3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Matrix LED Headlamp RHS shattered", "Adaptive Cruise Radar recalibration needed", "Authorized Audi invoice"]},
                {"id": "EVD-016-2", "name": "audi_itemized_quote.pdf", "type": "estimate", "source": "Audi South Mumbai Authorized", "size": "1.2 MB", "hash": "8800polaud2025e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495", "notes": ["Verified OEM Matrix Unit: ₹2,25,000", "Sensor module: ₹1,80,000", "Bumper & labor: ₹2,45,000", "Total: ₹6,50,000"]}
            ],
            "contradictions": [],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP-016-A",
                    "title": "Ramp Barrier Corner Graze",
                    "support_level": "Fully Verified & Corroborated",
                    "probability_score": 0.98,
                    "summary": "Damage strictly confined to corner lighting and ADAS sensors, matching freeway barrier height.",
                    "supporting_evidence": ["EVD-016-1", "EVD-016-2"],
                    "contradicting_evidence": [],
                    "assumptions": ["Zero alcohol involved; valid DL verified"]
                }
            ],
            "evaluation": {
                "physical_plausibility": {"status": "Mechanically Consistent", "score": 95, "details": "Impact angle and radar sensor displacement match ramp curvature."},
                "environmental_feasibility": {"status": "Verified", "score": 94, "details": "Clear evening conditions on freeway."},
                "damage_consistency": {"status": "Aligned", "score": 96, "details": "Damage limited strictly to left front lighting assembly."},
                "repair_anomaly": {"status": "Authorized Tariff Verified", "score": 92, "details": "Parts pricing aligns within 2% of Audi India master parts list."}
            },
            "recommendations": [
                {
                    "rec_id": "REC-016-1",
                    "action": "Executive Sign-Off Recorded (Chief Compliance Officer)",
                    "priority": "Critical",
                    "uncertainty_addressed": "IRDAI ₹5L Guardrail: Verified and formally authorized by Chief Compliance Officer",
                    "expected_information_gain": 0.99,
                    "materiality": 0.99,
                    "reliability": 0.99,
                    "cost": 0.05,
                    "rank_score": 6.53,
                    "status": "completed",
                    "responsible": "Chief Compliance Officer"
                }
            ],
            "settlement": {
                "eligible_repair": 650000,
                "deductible": 5000,
                "depreciation_deduction": 0,
                "salvage_allowance": 15000,
                "indicative_payout": 630000,
                "currency": "INR",
                "policy_clause": "EXECUTIVE AUTHORIZED: High-impact claim (> ₹5 Lakhs) reviewed and approved by Chief Compliance Officer. Full Zero-Dep indemnity cleared."
            }
        }
    ]

    total_claims = len(scenarios)
    print(f"[*] Inserting {total_claims} comprehensive claim scenarios and relational records...")

    # Iterate over scenarios and populate all 22 collections
    for sc in scenarios:
        cid = sc["claim_id"]
        v = sc["vehicle"]
        p = sc["policy"]

        # A. vehicles
        v_doc = {
            "vehicle_id": v["vehicle_id"],
            "claim_id": cid,
            "registration_number": v["registration"],
            "vin": v["vin"],
            "make": v["make"],
            "model": v["model"],
            "year": v["year"],
            "color": v["color"],
            "body_type": v["body_type"],
            "created_at": now
        }
        db.vehicles.insert_one(v_doc)

        # B. policies & policy_versions
        p_doc = {
            "policy_id": p["policy_id"],
            "claim_id": cid,
            "policy_number": p["policy_number"],
            "holder_name": p["holder"],
            "coverage_type": p["coverage_type"],
            "effective_from": p["start_date"],
            "effective_to": p["end_date"],
            "deductible_amount": p["deductible"],
            "sum_insured_limit": p["coverage_limit"],
            "depreciation_waiver": p.get("depreciation_waiver", False),
            "status": "active",
            "created_at": now
        }
        db.policies.insert_one(p_doc)

        # Version 1 and Version 2 (for timeline change demonstration)
        db.policy_versions.insert_one({
            "version_id": f"VER-{p['policy_id']}-1",
            "policy_number": p["policy_number"],
            "version_number": 1,
            "effective_from": p["start_date"],
            "effective_to": p["end_date"],
            "deductible": p["deductible"],
            "endorsements": ["Zero Depreciation Rider", "Engine Protector"],
            "created_at": now
        })

        # C. claims
        c_doc = {
            "claim_id": cid,
            "title": sc["title"],
            "scenario_type": sc["scenario_type"],
            "status": sc["status"],
            "priority": sc["priority"],
            "priority_score": sc["priority_score"],
            "claimant": sc["claimant"],
            "vehicle_reg": v["registration"],
            "policy_number": p["policy_number"],
            "incident_date": sc["incident"]["date"],
            "incident_time": sc["incident"]["time"],
            "incident_location": sc["incident"]["location"],
            "accident_type": sc["incident"]["accident_type"],
            "reported_narrative": sc["incident"]["narrative"],
            "estimated_damage": sc["incident"]["damage_estimate"],
            "third_party": sc["incident"]["third_party"],
            "assigned_investigator": "usr-inv-01",
            "created_at": now,
            "updated_at": now
        }
        db.claims.insert_one(c_doc)

        # D. evidence
        for ev in sc["evidence_items"]:
            # Generate physical sample image in backend/storage/uploads if generator exists
            local_rel_path = f"storage/uploads/{ev['name']}"
            if ev["type"] == "image" and create_sample_damage_image:
                create_sample_damage_image(ev["name"], sc["title"], f"{v['make']} {v['model']} ({v['registration']})", ev["notes"])
            elif create_sample_document_image:
                create_sample_document_image(ev["name"], ev["type"], [("Claim ID", cid), ("Vehicle", v["registration"]), ("Notes", ", ".join(ev["notes"]))])

            ev_doc = {
                "evidence_id": ev["id"],
                "claim_id": cid,
                "file_name": ev["name"],
                "file_type": ev["type"],
                "source": ev["source"],
                "file_size": ev["size"],
                "sha256_hash": ev["hash"],
                "storage_path": local_rel_path,
                "status": "processed",
                "notes": ev["notes"],
                "created_at": now
            }
            db.evidence.insert_one(ev_doc)

            # E. extracted_facts
            fact_doc = {
                "fact_id": f"FACT-{ev['id']}",
                "claim_id": cid,
                "evidence_id": ev["id"],
                "category": ev["type"],
                "extracted_text": "; ".join(ev["notes"]),
                "confidence_score": 0.94 if ev["type"] == "document" else 0.88,
                "verification_status": "verified" if sc["status"] == "investigation_completed" else "unverified",
                "created_at": now
            }
            db.extracted_facts.insert_one(fact_doc)

        # F. evidence_relationships
        for i, conf in enumerate(sc["contradictions"]):
            rel_doc = {
                "relationship_id": f"REL-{cid}-{i+1}",
                "claim_id": cid,
                "relationship_type": "Contradicts",
                "source_id": conf["sources_involved"][0] if conf["sources_involved"] else "Claimant-Narrative",
                "target_id": conf["sources_involved"][1] if len(conf["sources_involved"]) > 1 else "Physical-Damage",
                "severity": conf["severity"],
                "explanation": conf["description"],
                "materiality": conf["materiality"],
                "alternative_explanations": conf["alternative_explanations"],
                "resolution_evidence": conf["resolution_evidence"],
                "confidence": 0.89,
                "created_at": now
            }
            db.evidence_relationships.insert_one(rel_doc)

        # G. witness_statements
        db.witness_statements.insert_one({
            "statement_id": f"STMT-{cid}-01",
            "claim_id": cid,
            "speaker_name": sc["claimant"]["name"],
            "speaker_role": "claimant_driver",
            "statement_text": sc["incident"]["narrative"],
            "impact_direction_stated": sc["incident"]["accident_type"],
            "credibility_score": 0.85,
            "created_at": now
        })

        # H. investigation_timelines
        db.investigation_timelines.insert_one({
            "timeline_id": f"TIME-{cid}-1",
            "claim_id": cid,
            "event_type": "reported_accident_moment",
            "event_timestamp": f"{sc['incident']['date']}T{sc['incident']['time']}Z",
            "timestamp_type": "event_time",
            "description": f"Reported accident event: {sc['incident']['accident_type']}",
            "source_reference": "Claimant First Notice of Loss",
            "is_uncertain": False,
            "created_at": now
        })
        db.investigation_timelines.insert_one({
            "timeline_id": f"TIME-{cid}-2",
            "claim_id": cid,
            "event_type": "evidence_intake",
            "event_timestamp": now,
            "timestamp_type": "upload_time",
            "description": f"Multimodal evidence package uploaded and indexed",
            "source_reference": "CLAIMSIGHT Autonomous Intake Pipeline",
            "is_uncertain": False,
            "created_at": now
        })

        # I. accident_hypotheses
        for hyp in sc["hypotheses"]:
            db.accident_hypotheses.insert_one({
                "hypothesis_id": hyp["hypothesis_id"],
                "claim_id": cid,
                "title": hyp["title"],
                "support_level": hyp["support_level"],
                "probability_score": hyp["probability_score"],
                "summary": hyp["summary"],
                "supporting_evidence": hyp["supporting_evidence"],
                "contradicting_evidence": hyp["contradicting_evidence"],
                "assumptions": hyp["assumptions"],
                "created_at": now
            })

        # J. claim_evaluations
        db.claim_evaluations.insert_one({
            "evaluation_id": f"EVAL-{cid}",
            "claim_id": cid,
            "physical_plausibility": sc["evaluation"]["physical_plausibility"],
            "environmental_feasibility": sc["evaluation"]["environmental_feasibility"],
            "damage_consistency": sc["evaluation"]["damage_consistency"],
            "repair_anomaly": sc["evaluation"]["repair_anomaly"],
            "overall_integrity_rating": "High Reliability" if sc["scenario_type"] == "consistent_accident" else "Review Required",
            "created_at": now
        })

        # K. repair_estimates
        db.repair_estimates.insert_one({
            "estimate_id": f"EST-{cid}",
            "claim_id": cid,
            "workshop_name": "Authorized Regional Repair Center",
            "total_submitted_amount": sc["incident"]["damage_estimate"],
            "currency": "INR",
            "line_items": [
                {"description": f"{v['make']} {v['model']} Primary Impact Restoration", "part_cost": sc["incident"]["damage_estimate"] * 0.7, "labor_cost": sc["incident"]["damage_estimate"] * 0.2, "paint_cost": sc["incident"]["damage_estimate"] * 0.1}
            ],
            "is_flagged_anomaly": sc["scenario_type"] in ["cost_inflation", "incomplete_estimate"],
            "created_at": now
        })

        # L. evidence_requests (Next-Best-Evidence Intelligence)
        for rec in sc["recommendations"]:
            db.evidence_requests.insert_one({
                "request_id": rec["rec_id"],
                "claim_id": cid,
                "action_recommended": rec["action"],
                "priority": rec["priority"],
                "uncertainty_addressed": rec["uncertainty_addressed"],
                "expected_information_gain": rec["expected_information_gain"],
                "materiality": rec["materiality"],
                "reliability": rec["reliability"],
                "estimated_cost": rec["cost"],
                "rank_score": rec["rank_score"],
                "status": rec["status"],
                "responsible_party": rec["responsible"],
                "created_at": now
            })

        # M. investigation_reports
        is_high_impact = sc["incident"]["damage_estimate"] >= 500000
        is_investigated = sc["status"] != "intake_pending"

        db.investigation_reports.insert_one({
            "report_id": f"RPT-{cid}",
            "claim_id": cid,
            "title": f"Investigation Intelligence Report: {cid}",
            "status": "published" if is_investigated else "pending_investigation",
            "is_investigated": is_investigated,
            "is_high_impact": is_high_impact,
            "requires_executive_verification": is_high_impact,
            "settlement_calculation": sc["settlement"],
            "executive_summary": (
                f"Autonomous multimodal investigation complete for {v['year']} {v['make']} {v['model']}. "
                f"Identified {len(sc['contradictions'])} key contradictions and {len(sc['hypotheses'])} competing accident hypotheses."
                if is_investigated else f"Fresh intake dossier for {v['year']} {v['make']} {v['model']} awaiting surveyor inspection."
            ),
            "generated_by": "CLAIMSIGHT Autonomous Engine v3.1",
            "created_at": now
        })

        # N. investigator_decisions
        if sc["status"] == "investigation_completed" and is_high_impact:
            dec_status = "approved"
            dec_officer = "Chief Compliance Officer (Executive)"
            dec_officer_id = "usr-admin-01"
            dec_notes = "Executive Sign-Off Granted: High-impact claim (> ₹5 Lakhs) independently verified and authorized by Top Insurance Officer."
            verified_by_top = True
        elif sc["status"] == "investigation_completed":
            dec_status = "approved"
            dec_officer = "Senior SIU Investigator Sarah Chen"
            dec_officer_id = "usr-inv-01"
            dec_notes = "All facts corroborated and verified against benchmarks. Settlement approved."
            verified_by_top = True
        elif sc["status"] == "claim_rejected":
            dec_status = "rejected"
            dec_officer = "Senior SIU Investigator Sarah Chen"
            dec_officer_id = "usr-inv-01"
            dec_notes = "Repudiated: Statutory driver license breach confirmed via Parivahan RTO database."
            verified_by_top = True
        elif sc["status"] == "escalated_to_siu":
            dec_status = "escalated"
            dec_officer = "Senior SIU Investigator Sarah Chen"
            dec_officer_id = "usr-inv-01"
            dec_notes = "Guardrail Active: Estimated loss exceeds ₹5 Lakhs threshold. Escalated to Chief Compliance Officer for mandatory executive sign-off."
            verified_by_top = False
        else:
            dec_status = "decision_pending"
            dec_officer = "Senior SIU Investigator Sarah Chen"
            dec_officer_id = "usr-inv-01"
            dec_notes = "Multimodal evidence, hypotheses, and Next-Best-Evidence recommendations under active SIU review."
            verified_by_top = False

        db.investigator_decisions.insert_one({
            "decision_id": f"DEC-{cid}",
            "claim_id": cid,
            "investigator_id": dec_officer_id,
            "investigator_name": dec_officer,
            "is_high_impact": is_high_impact,
            "verified_by_top_insurance_officer": verified_by_top,
            "status": dec_status,
            "notes": dec_notes,
            "created_at": now
        })

        # O. audit_logs
        db.audit_logs.insert_one({
            "log_id": f"AUD-{cid}-1",
            "claim_id": cid,
            "user_id": "usr-admin-01",
            "action": "CLAIM_INGESTION_AND_AUTO_ANALYSIS",
            "details": f"Ingested {len(sc['evidence_items'])} multimodal assets and synthesized evidence relationship graph.",
            "timestamp": now
        })

        # P. notifications
        db.notifications.insert_one({
            "notification_id": f"NOTIF-{cid}",
            "user_id": "usr-inv-01",
            "claim_id": cid,
            "message": f"Claim {cid}: {sc['title']} flagged with priority score {sc['priority_score']}.",
            "read": False,
            "created_at": now
        })

        # Q. external_data_records
        db.external_data_records.insert_one({
            "record_id": f"EXT-{cid}-1",
            "claim_id": cid,
            "source": "OpenWeather-Historical-Reanalysis",
            "data": {"location": sc["incident"]["location"], "date": sc["incident"]["date"], "status": "retrieved"},
            "created_at": now
        })

        # R. counterfactual_scenarios
        db.counterfactual_scenarios.insert_one({
            "scenario_id": f"COUNT-{cid}-1",
            "claim_id": cid,
            "name": "Pre-Existing Exclusion Simulation",
            "hypothesis_tested": "What changes if the secondary impact is excluded as pre-existing?",
            "impact_on_settlement": -28000,
            "explanation": "Excluding front damage reduces total payable claim from ₹82,000 to ₹22,700.",
            "created_at": now
        })

    print(f"[OK] Successfully populated all 22 collections for all {total_claims} motor insurance claim scenarios (including high-impact > INR 5L and uninvestigated claims).")


if __name__ == "__main__":
    seed_database()
