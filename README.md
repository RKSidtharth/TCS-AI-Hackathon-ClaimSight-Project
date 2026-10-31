# CLAIMSIGHT AI
## Multimodal Autonomous Insurance Claims Investigator
*Decision-Support SIU Intelligence for Motor Vehicle Physical Damage Claims*

---

## 1. Executive Product Overview

**CLAIMSIGHT AI** is an enterprise-grade multimodal autonomous claims investigation platform engineered specifically for **motor vehicle insurance physical damage claims**.

When an accident occurs, insurance companies receive fragmented, contradictory, and unstructured evidence: accident photographs, claimant statements, witness accounts, police first-notice reports, repair bodyshop estimates, and policy documentation. Traditional claims assessment requires human investigators to manually cross-reference these sources, frequently missing subtle chronological discrepancies, pre-existing damage, or billing gouging.

CLAIMSIGHT AI serves as a **decision-support copilot** for Special Investigation Units (SIU):
1. **Multimodal Evidence Extraction**: Processes images, PDF repair estimates, police reports, and driver narratives.
2. **Evidence Relationship Graph**: Interactively links evidence and extracted facts into an interactive React Flow graph with cross-modal contradiction detection.
3. **Multi-Hypothesis Incident Reconstruction**: Evaluates competing hypotheses ($H_1, H_2, H_3$) rather than forcing a single hallucinated outcome.
4. **Multi-Dimensional Claim Evaluation**: Independently rates mechanical physical plausibility, environmental weather feasibility, damage aging consistency, and repair price benchmarks.
5. **Flagship Next-Best-Evidence Intelligence**: Employs an algorithmic ranking score based on Expected Information Gain (EIG), Materiality, and Collection Cost to recommend the single most decisive next forensic action.
6. **Policy Version & Coverage Engine**: Detects coverage transitions near midnight renewal dates and calculates deterministic, traceable settlement payouts.
7. **Explainable SIU PDF Reporting**: Generates downloadable 20-point forensic investigation reports with ReportLab.
8. **Human-in-the-Loop Governance**: Preserves human investigator authority over fraud allegations and final settlement approvals.

---

## 2. Mandatory Project Root Directory Structure

The project root strictly complies with the three-directory mandate:

```
CLAIMSIGHT-AI/
│
├── frontend/             # React 19 + TypeScript + Vite + Tailwind CSS + React Flow
│   ├── src/
│   │   ├── components/   # Navbar, Sidebar, and UI components
│   │   ├── context/      # AuthContext with Judge Persona quick-switch
│   │   ├── pages/        # Dashboard, Claims, Workspace, Evidence, Analytics, Settings
│   │   ├── services/     # Axios API client with automatic JWT bearer handling
│   │   └── types/        # TypeScript interfaces
│   ├── package.json
│   └── vite.config.ts
│
├── backend/              # Python FastAPI + Pydantic + PyMongo + ReportLab
│   ├── app/
│   │   ├── ai/           # Computer vision, OCR, NLP, hypotheses, plausibility, NBE
│   │   ├── api/          # Modular REST endpoints (auth, claims, evidence, reports)
│   │   ├── auth/         # JWT and BCrypt security
│   │   ├── core/         # MongoDB connection and environment settings
│   │   ├── schemas/      # Pydantic request/response models
│   │   ├── services/     # StorageService (SHA-256 & EXIF) and AuditService
│   │   └── main.py       # FastAPI application entrypoint
│   ├── storage/          # Forensic uploads and generated PDF reports
│   ├── tests/            # Pytest automated test suite
│   ├── requirements.txt
│   └── .env
│
└── database/             # MongoDB Schema, Indexes, Documentation & Seed
    ├── indexes/          # setup_indexes.py (optimized compound/unique indexes)
    ├── initialization/   # init_db.py (one-step database setup)
    ├── models/           # Pydantic schemas for 22 collections
    ├── seed/             # seed_data.py (10 interconnected synthetic scenarios)
    ├── documentation/    # Database architecture documentation
    └── database_setup.md
```

---

## 3. Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | React 19, TypeScript, Vite 8, Tailwind CSS v4, Lucide Icons, React Flow |
| **Backend API** | Python 3.12, FastAPI, Pydantic v2, PyMongo, PyJWT, BCrypt |
| **Database** | MongoDB Server (22 collections with unique & compound indexes) |
| **Forensic Storage** | Abstract local storage engine with SHA-256 fingerprinting & EXIF parsing |
| **Computer Vision** | OpenCV image analysis (edge contour density, RGB histograms, damage bounds) |
| **Document OCR** | Structured document extraction for policy terms, repair invoices, and police logs |
| **PDF Reporting** | ReportLab Platypus engine generating 20-point SIU reports |
| **Testing** | Pytest, FastAPI TestClient, Vite TS build |

---

## 4. Flagship Innovation: Next-Best-Evidence Intelligence

Rather than a static checklist of missing documents, CLAIMSIGHT AI calculates an algorithmic heuristic ranking score for every potential investigative action:

$$\text{Score}(\text{Action}) = \frac{\text{Expected Information Gain (EIG)} \times \text{Materiality} \times \text{Reliability}}{\text{Estimated Collection Cost} + \epsilon}$$

Where:
- **EIG**: The mathematical reduction in entropy across competing accident hypotheses ($H_1$ vs. $H_2$).
- **Materiality**: Financial impact of the targeted uncertainty relative to total claim value.
- **Reliability**: Evidentiary weight of the forensic source (e.g., EDR black box: 0.99 vs. bystander statement: 0.70).
- **Cost**: Monetary and operational friction of obtaining the asset.
- **$\epsilon$**: Small smoothing constant ($0.10$).

### Autonomous Re-Investigation Loop
When an investigator or claimant uploads new evidence:
1. File is fingerprinted with SHA-256 and duplicate-checked across the database.
2. EXIF geolocation and timestamps are forensically inspected.
3. AI pipeline extracts structured facts and damage bounding boxes.
4. Evidence relationships and cross-modal contradictions are re-evaluated.
5. Accident hypotheses probabilities are dynamically re-weighted.
6. Multi-dimensional claim evaluation and indicative settlement are refreshed.
7. Next-Best-Evidence recommendations are re-ranked in real-time.

---

## 5. Ten Interconnected Synthetic Claim Scenarios

All 10 scenarios are pre-loaded into MongoDB:

1. **`CLM-2026-001` (Consistent Rear-End)**: Honda City rear bumper dent matched by police station diary and benchmark estimate. Clear settlement approved.
2. **`CLM-2026-002` (Unexplained Front Damage)**: Hyundai Creta reported sole rear bump; photos reveal crumpled front-left fender with yellow paint scrape. Multi-hypothesis: secondary guardrail rebound vs pre-existing damage. Next-Best-Evidence requests front impact absorber inspection.
3. **`CLM-2026-003` (Oxidized Pre-Existing Damage)**: Maruti Swift door dent exhibits deep iron-oxide rust patina and paint flaking. Corrosion kinetics prove 4-week-old damage predating 24-hour-old notified loss.
4. **`CLM-2026-004` (Conflicting Witness Statements)**: Toyota Innova intersection collision. Claimant asserts straight green; Traffic Warden testifies claimant executed an unauthorized right turn across traffic.
5. **`CLM-2026-005` (Recycled Photo EXIF Mismatch)**: Kia Seltos highway scrape. Photo EXIF header reveals capture date 92 days prior in Mumbai, contradicting Bengaluru crash date.
6. **`CLM-2026-006` (Unitemized Bodyshop Estimate)**: Mahindra XUV700 submitted lump-sum ₹1,45,000 estimate lacking OEM part numbers or labor hours. Flagged for IRDAI Form 10 compliance.
7. **`CLM-2026-007` (Dynamic Cost Inflation)**: Tata Nexon EV headlamp quoted at ₹85,000 (+220% over regional OEM benchmark of ₹26,500). Benchmark engine recalibrates approved indemnity.
8. **`CLM-2026-008` (Midnight Policy Coverage Borderline)**: Volkswagen Virtus crash at 23:48 on March 14. Engine detects Policy v1 (Zero-Dep) expired at 23:59:59, confirming full zero-depreciation coverage.
9. **`CLM-2026-009` (Meteorological Discrepancy)**: Skoda Slavia hydroplaning claim. IMD radar telemetry records 0.0mm rainfall and 34°C dry asphalt.
10. **`CLM-2026-010` (Accordion Multi-Car Ambiguity)**: MG Hector 3-car highway pileup. Lead vehicle reports 2 impacts. Next-Best-Evidence requests Bosch EDR airbag crash pulse records to resolve sequence.

---

## 6. How to Run Locally

### Prerequisites
- Python 3.10+ (Tested on Python 3.12.8)
- Node.js 18+ (Tested on Node 20.19.5 & npm 10.8.2)
- MongoDB Server running on `localhost:27017`

### Step 1: Initialize Database & Seed 10 Scenarios
Run from the project root:
```powershell
python database/initialization/init_db.py
```

### Step 2: Start FastAPI Backend Server
```powershell
Set-Location backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

### Step 3: Start React Frontend Application
Open a second terminal window:
```powershell
Set-Location frontend
npm run dev
```
Access the application at: `http://localhost:3000`

---

## 7. Default Demonstration Credentials

The application includes a **Demo Persona Switcher** on the top navigation bar for 1-click testing:

| Persona | Email | Password | Role |
| :--- | :--- | :--- | :--- |
| **Senior SIU Investigator** | `investigator@claimsight.ai` | `Investigator2026!` | Full investigation workspace, React Flow graph, decision sign-off |
| **Chief Compliance Officer** | `admin@claimsight.ai` | `ClaimsightAdmin2026!` | Executive metrics, model registry, and deletion authority |
| **Policyholder** | `claimant@claimsight.ai` | `Claimant2026!` | Intake filing, evidence upload, and settlement status |

---

## 8. Verification & Test Execution

Run the backend automated test suite:
```powershell
Set-Location backend
python -m pytest tests/test_api.py -v
```
All tests verify health check, authentication, claim listing, Next-Best-Evidence formula calculation, analytics dashboard, and dynamic PDF generation.

