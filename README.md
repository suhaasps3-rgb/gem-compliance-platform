<div align="center">

<h1>SATARK</h1>
<p><strong>Smart Automated Tendering and Regulatory Kompetence</strong></p>
<p>An AI-powered compliance verification platform for India's Government e-Marketplace (GeM)</p>

<br/>

[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

</div>

---

## Overview

Government procurement in India involves verifying dozens of documents per bidder — GST certificates, Udyam registrations, CA-certified turnover certificates, work orders, EPFO/ESIC records — entirely by hand. This is slow, error-prone, and vulnerable to fraud.

**SATARK** automates this process end-to-end. It parses documents, builds an evidence graph, detects contradictions and forgeries, scores bidder compliance, and flags cartelization — giving procurement officers a single, auditable dashboard to make fast and legally defensible decisions.

---

## Features

### Document Intelligence
- **AI Document Parsing** — Forensic PDF analysis extracts structured data from GST certificates, Udyam registrations, CA turnover certificates, work orders, EPFO, ESIC, NSIC, ITR, and more — no third-party OCR API required
- **Visual Authenticity Check** — Detects missing authorized signatures and rubber stamps; triggers a compliance penalty and dashboard alert
- **UDIN Verification** — Validates CA UDIN format and flags missing or malformed identifiers

### Fraud & Forgery Detection
- **Identity Mismatch Detection** — If a bidder submits a document belonging to another entity, SATARK detects the company name mismatch and **blocks the compliance score** with a FORGERY ALERT
- **Contradiction Engine** — Cross-references claims across documents (e.g. MCA-reported turnover vs CA certificate) and surfaces discrepancies as evidence graph conflicts

### Anti-Cartelization
- **Cross-Bidder Analysis** — Scans all bidders in a tender for shared directors (MCA data), identical bid structures, correlated pricing patterns, and timing anomalies that indicate coordinated bidding

### Compliance Scoring
- **0–100 Compliance Score** — Aggregated from document verifications, graph contradictions, experience validation, technical spec matching, and visual authenticity
- **Risk Classification** — LOW / MEDIUM / HIGH / CRITICAL / ⛔ BLOCKED
- **Live Dashboard** — Score updates in real time as documents are uploaded

### Batch Processing
- **Multi-Bidder Batch Mode** — Upload a ZIP of all tender submissions; SATARK scores every bidder simultaneously with full breakdowns

### Officer Workflow
- **AI Recommendation Engine** — Provides Approve / Request Clarification / Reject with reasoning and red flags
- **Procurement Officer Final Review** — Human officer makes the authoritative, legally defensible decision
- **Immutable Audit Trail** — Every decision is hashed and logged; full evidence provenance graph maintained

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         React Frontend                          │
│                                                                 │
│  ┌─────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │  PDF Viewer │  │ Compliance       │  │  Evidence Graph   │  │
│  │  + Upload   │  │ Dashboard        │  │  Visualizer       │  │
│  └─────────────┘  └──────────────────┘  └───────────────────┘  │
│  ┌─────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │ Batch Mode  │  │ Tender           │  │  Contradiction    │  │
│  │ Processor   │  │ Configurator     │  │  Review           │  │
│  └─────────────┘  └──────────────────┘  └───────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │  REST API
┌─────────────────────────────▼───────────────────────────────────┐
│                        FastAPI Backend                          │
│                                                                 │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │  Document    │  │ Evidence      │  │  Collusion           │  │
│  │  Parsers     │  │ Graph Engine  │  │  Engine              │  │
│  │  (PyMuPDF)   │  │ (NetworkX)    │  │  (Cross-bidder)      │  │
│  └──────────────┘  └───────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │  Visual Auth │  │ Batch Engine  │  │  Audit Engine        │  │
│  │  (Signature  │  │ (Multi-bidder │  │  (Immutable log)     │  │
│  │   Detection) │  │  scoring)     │  │                      │  │
│  └──────────────┘  └───────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend Framework | React 18 + Vite 5 |
| Styling | Tailwind CSS |
| State Management | Zustand |
| PDF Rendering | react-pdf |
| Backend Framework | FastAPI + Uvicorn |
| PDF Analysis | PyMuPDF (fitz) |
| PDF Generation | ReportLab |
| Graph Engine | NetworkX |
| Runtime | Python 3.11 |
| Frontend Deployment | Vercel |
| Backend Deployment | Render |

---

## Supported Documents

| Document | Key Extracted Fields |
|---|---|
| GST Certificate | GSTIN, taxpayer type, composition status |
| Udyam Registration | MSME category, investment, turnover cap |
| CA Turnover Certificate | Annual turnover (Cr), UDIN, CA name, financial year |
| Work Orders | Order value, client, date, execution status |
| EPFO Statement | Contribution status, employee count, compliance |
| ESIC Registration | Establishment code, contribution compliance |
| NSIC Certificate | Product categories, EMD exemption eligibility |
| Startup India | DPIIT recognition, eligibility status |
| ITR Acknowledgement | PAN, assessment year, acknowledgement number |
| Debarment Check | Active debarment periods, blacklist status |

---

## Compliance Score

| Score | Risk Level | Recommended Action |
|---|---|---|
| 80 – 100 | 🟢 LOW | Approve |
| 60 – 79 | 🟡 MEDIUM | Minor clarifications |
| 40 – 59 | 🟠 HIGH | Mandatory officer review |
| 0 – 39 | 🔴 CRITICAL | Reject / Investigate |
| — | ⛔ BLOCKED | Forgery detected — score suppressed |

Score deductions are applied for: missing/invalid GSTIN, non-MSME entity, EPFO non-compliance, experience shortfall, technical spec failures, missing signature/stamp, active contradictions, and document identity mismatches.

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local: set VITE_API_URL=http://localhost:8000
npm run dev
```

App will be available at `http://localhost:5173`

---

## Environment Variables

### Frontend (`frontend/.env.local`)

| Variable | Description | Default |
|---|---|---|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` |

---

## Project Structure

```
gem-compliance-platform/
├── backend/
│   ├── main.py                  # FastAPI app + all endpoints
│   ├── document_parsers.py      # PDF parsing for all document types
│   ├── graph_engine.py          # Evidence graph + contradiction detection
│   ├── collusion_engine.py      # Cross-bidder cartelization analysis
│   ├── batch_engine.py          # Multi-bidder batch scoring
│   ├── visual_authenticity.py   # Signature + stamp detection
│   ├── experience_engine.py     # Work order experience validation
│   ├── technical_eval.py        # Technical specification matching
│   ├── audit_engine.py          # Immutable decision audit trail
│   ├── rule_compiler.py         # AI tender rule extraction
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── Dashboard.jsx        # Main compliance dashboard
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ComplianceScorecard.jsx
│   │   │   ├── TurnoverVerificationCard.jsx
│   │   │   ├── ExperiencePanel.jsx
│   │   │   ├── TechnicalMatrix.jsx
│   │   │   ├── BatchProcessor.jsx
│   │   │   └── PdfViewer/
│   │   └── store/
│   │       └── dashboardStore.js
│   └── public/                  # Demo PDF documents
├── database/
│   └── mock_dataset.json        # Demo bidder data
├── vercel.json
└── render.yaml
```

---

## Team

Built by:

- **Suhaas** 
- **Sathvika Methuku**
- **Akshaya Mamilla**
- **Mohammed Muzammil Ahmed**
- **Vishwak Mylavarapu**
- **Pranay Kumar Nangunoori**

---

## License

This project is licensed under the [MIT License](LICENSE).
