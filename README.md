# CLAIMSIGHT AI
## Multimodal Autonomous Insurance Claims Investigator
*Enterprise Decision-Support SIU Intelligence for Motor Vehicle Physical Damage Claims*

---

## 1. Executive Product Overview

**CLAIMSIGHT AI** is an enterprise-grade multimodal autonomous claims investigation platform engineered specifically for **motor vehicle insurance physical damage claims**.

When an accident occurs, insurance companies receive fragmented, contradictory, and unstructured evidence: accident photographs, claimant statements, witness accounts, police General Diary (GD) and First Information Reports (FIR), repair bodyshop estimates, and policy documentation. Traditional claims assessment requires human investigators to manually cross-reference these sources, frequently missing subtle chronological discrepancies, pre-existing damage, or billing gouging.

CLAIMSIGHT AI serves as a **decision-support copilot** for Special Investigation Units (SIU):
1. **Multimodal Evidence Extraction**: Processes exterior vehicle photographs, PDF repair estimates, police GD/FIR extracts, and driver statements.
2. **YOLOv8 Neural Vision Damage Decomposition**: Localizes primary structural deformation, classifies damage types, maps bounding box coordinates, and detects spatial zone mismatches (e.g. consumer claims front damage while YOLO neural vision identifies rear bumper impact).
3. **Priority Reference #1 (Police File vs Consumer Statement)**: Evaluates consistency between the driver's declaration and the official attending police officer's General Diary record, alternating uniformly between verified corroboration and critical discrepancy.
4. **Interactive Evidence Relationship Graph**: Interactively links evidence assets and extracted facts into an interactive React Flow graph with cross-modal contradiction detection.
5. **Multi-Hypothesis Incident Reconstruction**: Evaluates competing physical explanations ($H_1, H_2, H_3$) rather than forcing a single hallucinated outcome.
6. **5D Multidimensional Claim Evaluation**: Independently rates mechanical physical plausibility, environmental weather feasibility, damage aging consistency, documentary integrity, and repair price benchmarks.
7. **Flagship Next-Best-Evidence (NBE) Intelligence**: Employs an algorithmic ranking score based on Expected Information Gain (EIG), Materiality, and Collection Cost to recommend the single most decisive next forensic action.
8. **High-Impact Loss Guardrail (> ₹5 Lakhs)**: Enforces IRDAI compliance by blocking standard investigators from approving losses exceeding ₹5,00,000 without mandatory Chief Compliance Officer authorization.
9. **Explainable Dual PDF Reporting**: Generates both downloadable 20-point SIU Forensic Investigation Reports and Certified Official Police FIR / GD extracts using ReportLab.
10. **Human-in-the-Loop Governance**: Preserves human investigator authority over fraud allegations and final settlement approvals.

---

## 2. Mandatory Project Root Directory Structure

The project root strictly complies with the three-directory mandate:

```
CLAIMSIGHT-AI/
├── frontend/             # React 19 + TypeScript + Vite + Tailwind CSS + React Flow
│   ├── src/
│   │   ├── components/   # Navbar, Sidebar, and UI components
│   │   ├── context/      # AuthContext with Judge Persona quick-switch
│   │   ├── pages/        # Dashboard, Claims, Workspace, Evidence, Analytics, Settings
│   │   ├── services/     # Axios API client with automatic JWT bearer handling
│   │   ├── types/        # TypeScript interfaces
│   │   └── utils/        # Dynamic vehicle imagery and formatting
│   ├── package.json
│   └── vite.config.ts
├── backend/              # FastAPI + Python + PyMongo + YOLO Computer Vision + ReportLab
│   ├── app/
│   │   ├── ai/           # Computer vision, NLP, contradiction, reconstruction engines
│   │   ├── api/          # FastAPI REST endpoints (claims, evidence, reports, auth)
│   │   ├── auth/         # JWT security and role-based access control
│   │   ├── core/         # MongoDB connection with serverless in-memory fallback
│   │   ├── schemas/      # Pydantic validation models
│   │   └── services/     # Audit logging and storage services
│   ├── tests/            # Automated Pytest suite (16 test cases)
│   └── requirements.txt
├── database/             # Schemas, seeding scripts, and data models
│   ├── models/           # Pydantic schema models
│   ├── seed/             # Complete 22-collection synthetic database seeder
│   └── database_setup.md
├── vercel.json           # Cloud deployment configuration
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation
```

---

## 3. How to Run the Project Locally

Follow these steps to run both the frontend and backend servers on your local computer.

### Prerequisites
* **Node.js**: v18.0.0 or later ([Download Node.js](https://nodejs.org/))
* **Python**: v3.10, v3.11, or v3.12 ([Download Python](https://www.python.org/))
* **MongoDB** *(Optional)*: Local MongoDB running on `localhost:27017` or cloud MongoDB Atlas.
  > **Zero-Config Resilient Mode**: If local MongoDB is not running, the backend automatically activates an in-memory database (`mongomock`) pre-loaded with synthetic claims, so you can run the entire platform without installing MongoDB!

---

### Step 1: Clone the Repository
```powershell
git clone https://github.com/RKSidtharth/TCS-AI-Hackathon-ClaimSight-Project.git
cd TCS-AI-Hackathon-ClaimSight-Project
```

---

### Step 2: Set Up and Start the Backend Server

1. Open a terminal and navigate to the `backend/` directory:
   ```powershell
   cd backend
   ```

2. Create and activate a Python virtual environment:
   * **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install backend dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. *(Optional)* Seed the local MongoDB database with synthetic claims:
   ```powershell
   python -m database.seed.seed_data
   ```

5. Launch the FastAPI server:
   ```powershell
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

* The backend API will be live at: **[http://localhost:8000](http://localhost:8000)**
* Interactive Swagger API Documentation: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

### Step 3: Set Up and Start the Frontend Application

1. Open a **second terminal window** and navigate to the `frontend/` directory:
   ```powershell
   cd frontend
   ```

2. Install Node dependencies:
   ```powershell
   npm install
   ```

3. Start the Vite development server:
   ```powershell
   npm run dev -- --host 0.0.0.0 --port 3000
   ```

* The frontend application will be live at: **[http://localhost:3000](http://localhost:3000)**

---

## 4. How to Deploy to Vercel

The application is pre-configured for deployment to **Vercel** via `vercel.json`:

### Option A: 1-Click Deployment via GitHub (Recommended)
1. Go to **[vercel.com/new](https://vercel.com/new)** and sign in with your GitHub account.
2. Select your repository: **`RKSidtharth/TCS-AI-Hackathon-ClaimSight-Project`**.
3. Under **Project Settings**:
   * **Framework Preset**: Vite
   * **Root Directory**: `./` (leave default)
4. *(Optional Environment Variable)*:
   * `MONGODB_URI`: Your MongoDB Atlas connection string (e.g. `mongodb+srv://<user>:<password>@cluster.mongodb.net/claimsight_ai`).
   * *If omitted, the platform runs in high-performance Serverless In-Memory mode with all synthetic claims and reports active!*
5. Click **Deploy**. Vercel will build both the React frontend and FastAPI backend serverless functions.

### Option B: Deploy via Vercel CLI
```powershell
# In the project root:
npx vercel --prod
```

---

## 5. User Roles and Access Control

The platform provides a **Demo Persona Switcher** on the top navigation bar for immediate testing without manually typing credentials:

| Persona / Role | Email | Password | Allowed Capabilities |
| :--- | :--- | :--- | :--- |
| **Policyholder (Consumer)** | `claimant@claimsight.ai` | `Claimant2026!` | • Submit new claim with vehicle details & damage photos<br/>• View and track only their own registered claims<br/>• Strictly blocked from internal SIU investigation files |
| **Senior SIU Investigator** | `investigator@claimsight.ai` | `Investigator2026!` | • Access multimodal investigation workspace<br/>• Inspect YOLO damage localization and bounding boxes<br/>• Interact with React Flow relationship graph<br/>• Run counterfactual "What-If" sandbox simulations<br/>• Download certified Police FIR / GD and SIU PDF reports<br/>• Sign off on standard claims (< ₹5 Lakhs) |
| **Chief Compliance Officer (Admin)** | `admin@claimsight.ai` | `ClaimsightAdmin2026!` | • All Senior Investigator capabilities<br/>• **Mandatory High-Impact Guardrail Authorization**: Exclusive authority to review and approve claims exceeding ₹5,00,000<br/>• View comprehensive synthetic database across all dossiers |

---

## 6. Core Forensic Features & Workflow Walkthrough

### 1. Consumer Intake & Vehicle Photo Reflection
* Policyholders navigate to **`/claims/new`** to submit a First Notice of Loss (FNOL).
* Includes vehicle registration, policy number, loss date/time, and an image upload dropzone.
* Uploaded photos are normalized via client-side canvas and saved faithfully to the dossier.
* The Chief Compliance Officer and Senior Investigator immediately view the exact consumer-uploaded photo in the investigation workspace.

### 2. YOLOv8 Neural Vision Damage Localization
* Computer vision neural analysis decomposes vehicle damage:
  * **Primary Zone**: `REAR`, `FRONT`, or `LATERAL` structural assembly.
  * **Identified Component**: e.g., *Rear Bumper / Lower Valence Assembly* or *Front Radiator Grille & Bumper Fascia*.
  * **Damage Classification**: e.g., *Direct Shunt Plastic Fracture* or *Structural Crumple & Lens Shatter*.
  * **Precision & ROI**: Overlaid with a dynamic targeting reticle displaying confidence score ($94\%$) and bounding box coordinates `[X, Y, W, H]`.
  * **Spatial Discrepancy Flagging**: If a consumer asserts front damage but YOLO detects rear damage (or vice-versa), a purple alert banner highlights the spatial contradiction.

### 3. Priority Reference #1: Police GD / FIR Corroboration vs Discrepancy
* Mandatory first-reference cross-examination comparing the consumer declaration against the attending police officer's General Diary (GD) record.
* Alternates uniformly:
  * **Corroborated Mode**: Shows a green verified badge confirming the driver's stationary position and sequence.
  * **Discrepancy Mode**: Flags a red critical alert indicating diverging impact dynamics recorded at the scene.
* **Downloadable Certified FIR (PDF)**: Both investigators and admins can download the certified police report PDF directly via the top action bar or forensic assets gallery.

### 4. Interactive Evidence Relationship Graph (React Flow)
* Renders evidence assets, extracted facts, and witness declarations as an interactive nodal graph.
* Nodes are color-coded (Claimant, Evidence, Police, Bodyshop Quote, Policy).
* Edges display evidential relationships (`Corroborates`, `Contradicts`, `Explains`, `Uncertain`).

### 5. Multi-Hypothesis Accident Reconstruction
* Eliminates AI hallucination by generating competing physical scenarios:
  * **$H_1$**: Primary Direct Kinetic Impact (Claimant Narrative)
  * **$H_2$**: Cumulative Multi-Event / Pre-Existing Damage Divergence
* Each hypothesis is rated with probability percentages, underlying assumptions, and supporting/conflicting evidence.

### 6. High-Impact Loss Guardrail (> ₹5,00,000 IRDAI Mandate)
* In compliance with IRDAI regulatory guidelines, claims exceeding ₹5 Lakhs activate a strict guardrail.
* Standard investigators are blocked with an HTTP 403 error if attempting autonomous approval.
* Executive approval is unlocked only when logged in as the Chief Compliance Officer (`admin@claimsight.ai`).

### 7. Dual Forensic PDF Downloads
* **SIU Forensic Investigation Report (PDF)**: Click **"Export SIU PDF Report"** to download a 20-point dossier including executive summary, evidence hashes, YOLO damage breakdown, cross-modal matrix, multi-hypothesis reconstruction, next-best-evidence rankings, and settlement calculations.
* **Official Police FIR / GD Extract (PDF)**: Click **"Download Police FIR / GD"** to download the certified police station extract issued under Section 154 Cr.P.C. / Section 173 BNSS 2023.

---

## 7. Automated Test Execution

Run the backend automated test suite verifying all 16 core capabilities:

```powershell
cd backend
python -m pytest tests/test_api.py -v
```

### Test Coverage Highlights:
* `test_health_check`: Server health and database connection.
* `test_auth_login_success` & `test_auth_login_invalid`: JWT token generation and role authorization.
* `test_high_impact_guardrail_blocks_standard_investigator`: Confirms standard investigators receive HTTP 403 on > ₹5L approvals.
* `test_high_impact_guardrail_allows_executive_admin`: Confirms Chief Compliance Officer can authorize high-impact claims.
* `test_claimant_strictly_isolated_from_other_claims_and_siu`: Enforces policyholder data privacy.
* `test_claim_creation_restricted_to_policyholder_with_image_reflection`: Verifies photo persistence and role enforcement.
* `test_siu_pdf_download_succeeds`: Validates binary PDF generation without exceptions.
* `test_yolo_detection_endpoint`: Verifies computer vision damage localization API.
* `test_fir_pdf_download_succeeds_for_investigator_and_direct`: Validates police FIR document generation.
* `test_fir_pdf_download_forbidden_for_claimant`: Verifies policyholders cannot access internal police files.

---

## 8. Technology Stack Summary

* **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, React Flow, Recharts, Lucide Icons, Axios.
* **Backend**: Python 3.12, FastAPI, Pydantic v2, PyMongo, PyJWT, Bcrypt, ReportLab (PDF), NumPy.
* **Database**: MongoDB (Local or MongoDB Atlas) with automatic Serverless in-memory fallback via Mongomock.
* **Deployment**: Git, Vercel, Uvicorn, Docker-compatible.

---

## 9. License

This project is licensed under the MIT License for the TCS AI Hackathon 2026.
