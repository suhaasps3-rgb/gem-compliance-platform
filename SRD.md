# Software Requirements Document (SRD)
**Project Name:** GeM Compliance Platform (Smart India Hackathon)
**Version:** 1.1

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Document (SRD) specifies the architecture, functional, and non-functional requirements for the GeM (Government e Marketplace) Compliance Platform. The system acts as a deterministic verification engine that cross-references unstructured bidder claims against authoritative government APIs.

### 1.2 Scope
The system will ingest Tender PDFs and Bidder Certificates, extract key metrics (Turnover, MSME Status, EMD), and map them into a **NetworkX Evidence Provenance Graph**. It will highlight contradictions (e.g., claimed turnover vs. MCA21 reported turnover) to Procurement Officers. It explicitly relies on deterministic math for rule evaluation, utilizing LLMs only for initial text structuring.

### 1.3 Definitions and Acronyms
- **GeM:** Government e Marketplace.
- **DPDP Act:** Digital Personal Data Protection Act (India).
- **GFR:** General Financial Rules (2017).
- **MCA21:** Ministry of Corporate Affairs database.
- **SHA-256:** Cryptographic hash algorithm used for the audit ledger.

---

## 2. Overall Description

### 2.1 Product Perspective
A standalone full-stack web application. 
- **Backend:** Python (FastAPI, NetworkX, PyMuPDF, Hashlib).
- **Frontend:** React (Vite, Tailwind CSS).
- **Architecture:** Microservices-ready, currently simulating external API integrations (Udyam, MCA21, GSTN) via JSON mocks.

### 2.2 User Classes
1. **Procurement Officer:** Views dashboards, evaluates contradiction cascades, and triggers statutory actions (Show-Cause notices).
2. **System Auditor / Vigilance:** Reviews the cryptographic hash chain to ensure no officer decisions were altered retroactively.

---

## 3. Functional Requirements

### 3.1 Document Ingestion & Extraction (`rule_compiler.py`)
- **REQ-1.1:** The system must accept binary PDF uploads.
- **REQ-1.2:** The system must extract text natively using PyMuPDF (zero-cost, low-latency).
- **REQ-1.3:** The system must dynamically identify compliance thresholds (e.g., "Turnover <= 10Cr") and output them as a structured JSON schema.

### 3.2 Evidence Provenance Graph (`graph_engine.py`)
- **REQ-2.1:** The system must construct a directed acyclic graph (DAG) linking Bidder -> Identity Anchor -> Claims -> Authoritative Evidence.
- **REQ-2.2:** The system must deterministically compare Claims vs Evidence (e.g., `8.5 <= 10.0`).
- **REQ-2.3:** If a contradiction is detected, the system must shift the bidder status to `NEEDS_REVIEW` and generate a human-readable AI Synthesis.

### 3.3 Cryptographic Audit Ledger (`audit_engine.py`)
- **REQ-3.1:** All officer decisions (e.g., "Generate Show-Cause Notice") must be securely logged.
- **REQ-3.2:** The system must aggressively scrub PII (e.g., Aadhaar numbers) via Regex prior to ledger entry to maintain **DPDP Act Compliance**.
- **REQ-3.3:** The system must generate a SHA-256 hash chaining the current decision to the previous decision's hash, ensuring mathematical immutability.

### 3.4 Cross-Bidder Collusion Engine (`collusion_engine.py`)
- **REQ-4.1:** The system must cross-reference all bidders within a tender to identify heuristic anomalies.
- **REQ-4.2:** Must flag shared MCA21 Directors and identical hidden PDF metadata.
- **REQ-4.3:** Must strictly label these overlaps as "Investigative Leads", not deterministic disqualifications.

---

## 4. User Interface Requirements

### 4.1 Contradiction Cascade UI
- Must display a split-screen view contrasting "Claimed Evidence" (Bidder) against "Authoritative Government Data" (API).
- Must utilize high-contrast alert colors (Red/Amber/Green) for rapid visual triage.

### 4.2 Tamper-Evident Modal
- Upon executing a statutory action, the UI must immediately display the generated **SHA-256 Hash** to the officer.
- Must display auto-generated legal notice text citing applicable laws (e.g., GFR 2017 Rule 175).

---

## 5. Non-Functional Requirements

### 5.1 Performance & Scalability
- **Latency:** Graph traversal and contradiction detection must resolve in `< 500ms`.
- **Cost-Optimization:** The system must default to native PyMuPDF extraction, routing to paid OCR APIs (AWS Textract) only if native extraction yields `< 50 characters` (indicating a scanned image).

### 5.2 Security & Compliance
- System must never auto-disqualify a bidder based purely on heuristic AI analysis.
- System architecture must assume internal threats (Rogue Sysadmin), mitigated by the continuous hashing of the Audit Ledger.
