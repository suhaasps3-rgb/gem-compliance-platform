# Software Requirements Document (SRD)
**Project Name:** GeM Compliance Platform (Smart India Hackathon)
**Version:** 2.0 (Architectural Polish Revision)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Document (SRD) specifies the architecture, functional, and non-functional requirements for the GeM (Government e Marketplace) Compliance Platform. The system acts as a deterministic verification engine that cross-references unstructured bidder claims against authoritative government APIs.

### 1.2 Scope
The system will ingest Tender PDFs to compile rules and Bidder Certificates to extract claims, mapping them into a **NetworkX Evidence Provenance Graph**. It will highlight contradictions to Procurement Officers. It explicitly relies on deterministic math for rule evaluation and Identity Anchoring (PAN/CIN). The current prototype utilizes targeted Regex/PyMuPDF for extraction to guarantee zero-latency and deterministic reliability, with LLM-based unstructured parsing scoped for Phase 2.

### 1.3 Definitions and Acronyms
- **GeM:** Government e Marketplace.
- **DPDP Act:** Digital Personal Data Protection Act (India).
- **GFR:** General Financial Rules (2017).
- **PAN / CIN / GSTIN:** Permanent Account Number / Corporate Identification Number / Goods and Services Tax Identification Number (Primary deterministic identity anchors).
- **Udyam:** MSME registration portal for the Government of India.
- **SHA-256:** Cryptographic hash algorithm used for the audit ledger.

---

## 2. Overall Description

### 2.1 Product Perspective
A standalone full-stack web application. 
- **Backend:** Python (FastAPI, NetworkX, PyMuPDF, Hashlib).
- **Frontend:** React (Vite, Tailwind CSS).
- **API Integration Strategy:** 
  - GSTN (via GSP ecosystem) and DigiLocker (OAuth 2.0) are architected as production-viable pathways. 
  - Udyam and MCA21 APIs are currently simulated via JSON mocks due to restricted government network access but are architected for seamless drop-in integration.

### 2.2 User Classes
1. **Procurement Officer:** Views dashboards, evaluates contradiction cascades, and triggers statutory actions (Show-Cause notices).
2. **System Auditor / Vigilance:** Reviews the cryptographic hash chain to ensure no officer decisions were altered retroactively.

---

## 3. Functional Requirements

### 3.1 Tender Rule Compilation (`rule_compiler.py`)
- **REQ-1.1:** The system must accept binary Tender PDF uploads.
- **REQ-1.2:** The system must extract text natively using PyMuPDF and dynamically identify compliance thresholds (e.g., "Turnover <= 10Cr").
- **REQ-1.3 (Regulatory Versioning Engine):** Extracted rules must be stored with effective dates and supersession flags, ensuring a tender issued in 2023 is strictly audited against 2023 regulatory limits, regardless of current policy.

### 3.2 Bidder Document Extraction & Ingestion
- **REQ-2.1:** The system must extract structured claims from bidder-submitted compliance documents (e.g., CA Certificates).
- **REQ-2.2:** The system must utilize a three-tier extraction pipeline: PyMuPDF native extraction (primary), falling back to OCR if character count is insufficient (indicating a scanned image). *Note: The current prototype implements the intelligent routing tripwire; actual AWS Textract OCR integration is scoped for Phase 2.*

### 3.3 Evidence Provenance Graph (`graph_engine.py`)
- **REQ-3.1 (Deterministic Anchoring):** The system must construct a Directed Graph (allowing bidirectional corroboration edges) heavily anchored on PAN as the primary deterministic key, explicitly cross-corroborating against the PAN embedded within the GSTIN. Fuzzy matching must be demoted and treated only as an investigative lead, never as authoritative evidence.
- **REQ-3.2 (Temporal Compliance):** The engine must evaluate evidence validity strictly as of the **Tender Closing Date**, not the current system date.
- **REQ-3.3 (State Model):** The system must evaluate compliance into five distinct states: `VERIFIED_COMPLIANT`, `NON_COMPLIANT`, `NEEDS_REVIEW` (contradiction detected), `UNVERIFIED` (API unreachable), and `NOT_APPLICABLE`.

### 3.4 Cryptographic Audit Ledger & Statutory Action (`audit_engine.py`)
- **REQ-4.1:** All officer decisions must trigger a statutory workflow referencing specific laws (e.g., GFR 2017 Rule 175 for misrepresentation, triggering Rule 151 Debarment).
- **REQ-4.2:** The system must aggressively scrub PII (e.g., Aadhaar numbers) via Regex prior to ledger entry to maintain **DPDP Act Compliance**.
- **REQ-4.3:** The system must generate a SHA-256 hash chaining the current decision to the previous decision's hash, ensuring mathematical immutability.

### 3.5 Cross-Bidder Collusion Engine (`collusion_engine.py`)
- **REQ-5.1:** The system must cross-reference all bidders within a tender to identify heuristic anomalies (e.g., shared MCA21 Directors, identical hidden PDF metadata).
- **REQ-5.2:** Must strictly label these overlaps as "Investigative Leads", not deterministic disqualifications.

---

## 4. User Interface Requirements

### 4.1 Contradiction Cascade UI
- Must display a split-screen view contrasting "Claimed Evidence" (Bidder) against "Authoritative Government Data" (API).
- Must utilize high-contrast alert colors (Red/Amber/Green) for rapid visual triage mapping to the Five-State compliance model.

### 4.2 Tamper-Evident Modal
- Upon executing a statutory action, the UI must immediately display the generated **SHA-256 Hash** to the officer to verify the ledger entry.

---

## 5. Non-Functional Requirements

### 5.1 Performance & Scalability
- **Latency:** Graph traversal and contradiction detection must resolve in **sub-second latency (< 1000ms)** for demo-scale graphs, achievable by executing NetworkX traversals entirely in-memory prior to database commit.
- **Cost-Optimization:** The system must default to native PyMuPDF extraction, routing to paid OCR APIs only if native extraction fails, saving significant operational expenditure at a national scale. *(OCR API integration is scoped for Phase 2).*

### 5.2 Security & Compliance
- System must never auto-disqualify a bidder based purely on heuristic AI analysis.
- System architecture must assume internal threats (Rogue Sysadmin), mitigated by the continuous hashing of the Audit Ledger.
