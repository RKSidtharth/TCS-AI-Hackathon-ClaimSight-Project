# CLAIMSIGHT AI - Database Architecture & Setup Guide

## 1. Overview
CLAIMSIGHT AI uses **MongoDB** as its primary document store, designed with high-performance compound indexing, referenced relationships, and embedded sub-documents for fast read-heavy investigative operations.

Large evidence binaries (photographs, dashcam clips, PDF repair estimates) are stored via an abstract storage engine (`backend/storage/uploads/` in local mode, or S3/Azure Blob in cloud deployments). The MongoDB database holds structured metadata, extracted facts, relationship graphs, timelines, and audit records.

---

## 2. Collections (22 Core Collections)

1. **`users`**: Administrative, investigator, and claimant accounts with bcrypt-hashed credentials and RBAC roles.
2. **`claims`**: Core insurance claim records with vehicle references, incident metadata, and workflow statuses.
3. **`vehicles`**: Insured and third-party vehicle specifications (VIN, registration, make, model, year, trim).
4. **`policies`**: Master policy details, coverage limits, deductibles, endorsements, and holder references.
5. **`policy_versions`**: Historical versions, endorsements, riders, effective date ranges, and cancellation logs.
6. **`evidence`**: Uploaded evidence items with SHA-256 hashes, EXIF metadata, source tags, and processing flags.
7. **`extracted_facts`**: Structured facts extracted by AI/OCR pipelines with confidence scores, source references, and verification status.
8. **`evidence_relationships`**: Graph edges connecting evidence items and facts (Supports, Contradicts, Corroborates, DerivedFrom, RequiresVerification).
9. **`witness_statements`**: Transcripts, claimant vs. third-party statements, impact directions, and divergence annotations.
10. **`investigation_timelines`**: Chronological events distinguishing incident timestamp, doc creation, upload time, and AI inferences.
11. **`accident_hypotheses`**: Competing incident reconstructions (H1, H2, H3...) with qualitative support ratings, assumptions, and counter-evidence.
12. **`claim_evaluations`**: Multidimensional assessments (physical plausibility, environmental feasibility, damage consistency, repair cost reasonableness).
13. **`repair_estimates`**: Line-item repair estimates, labor hours, paint costs, and component replacement flags.
14. **`repair_benchmarks`**: Regional benchmark repair and parts costs for anomaly detection and rate validation.
15. **`evidence_requests`**: Ranked Next-Best-Evidence recommendations and investigator request tracking.
16. **`investigation_reports`**: Generated explainable investigation reports and settlement recommendations.
17. **`investigator_decisions`**: Human-in-the-loop annotations, confirmed contradictions, approved settlements, and sign-offs.
18. **`audit_logs`**: Immutable audit trail of all claim access, status transitions, and data updates.
19. **`notifications`**: System and user alerts for missing evidence, review requests, and status changes.
20. **`model_registry`**: Active and historical AI/ML model versions (YOLO, OCR, Sentence Transformer, LLM prompt hashes).
21. **`external_data_records`**: Cached third-party records (verified historical weather, telematics, registry checks).
22. **`counterfactual_scenarios`**: What-if investigation sandboxes for hypothetical assumption testing.

---

## 3. Database Initialization & Seeding

### Prerequisites
- MongoDB Server running locally on `localhost:27017` or a MongoDB Atlas connection URI.

### Command to Initialize and Seed
Run from the project root:
```powershell
python database/initialization/init_db.py
```
This script:
1. Connects to `mongodb://localhost:27017/claimsight_ai` (or configured URI in `backend/.env`).
2. Creates all required collections and unique/compound indexes.
3. Inserts 10 realistic, interconnected synthetic motor insurance claim scenarios demonstrating the full investigation spectrum.
4. Registers default administrator, investigator, and claimant users.

---

## 4. Default Seed Credentials

| Role | Email | Password | Full Name |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@claimsight.ai` | `ClaimsightAdmin2026!` | Chief Compliance Officer |
| **Investigator** | `investigator@claimsight.ai` | `Investigator2026!` | Senior SIU Investigator Sarah Chen |
| **Claimant** | `claimant@claimsight.ai` | `Claimant2026!` | Rajesh Kumar (Policyholder) |

---

## 5. Indexes Strategy

- **`claims`**: `{ claim_id: 1 }` (unique), `{ status: 1, created_at: -1 }`, `{ policy_number: 1 }`, `{ vehicle_reg: 1 }`
- **`evidence`**: `{ evidence_id: 1 }` (unique), `{ claim_id: 1, created_at: 1 }`, `{ sha256_hash: 1 }`
- **`extracted_facts`**: `{ fact_id: 1 }` (unique), `{ claim_id: 1 }`, `{ evidence_id: 1 }`
- **`evidence_relationships`**: `{ relationship_id: 1 }` (unique), `{ claim_id: 1 }`, `{ source_id: 1, target_id: 1 }`
- **`accident_hypotheses`**: `{ hypothesis_id: 1 }` (unique), `{ claim_id: 1 }`
- **`audit_logs`**: `{ claim_id: 1, timestamp: -1 }`, `{ user_id: 1 }`
- **`repair_benchmarks`**: `{ make: 1, model: 1, component: 1 }`

