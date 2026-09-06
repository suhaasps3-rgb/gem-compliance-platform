# Software Requirements Specification (SRS)
**Project Name:** GeM Compliance Platform (Smart India Hackathon)
**Version:** 2.0 (Verified Architecture Release)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document details the functional and non-functional requirements for the GeM (Government e Marketplace) Compliance Platform. The system acts as a deterministic verification engine designed to automatically cross-reference unstructured bidder claims against authoritative government APIs, eliminating manual workloads while strictly preserving legal compliance.

### 1.2 Scope
The platform serves as an intelligent, mathematical middleware for government procurement officers. It ingests Bidder Certificates and extracts claims using deterministic Regex parsing, explicitly mapping them into an in-memory **Temporal Evidence Provenance Graph (NetworkX)**. It cross-verifies these claims against Identity Anchors (PAN/CIN). The system strictly enforces the principle of "AI proposes, Officer decides"—it never auto-disqualifies bidders, but surfaces contradictions and cryptographic logs onto a tamper-evident SHA-256 ledger.

### 1.3 Definitions and Acronyms
- **GeM:** Government e Marketplace.
- **DPDP Act:** Digital Personal Data Protection Act (India).
- **GFR:** General Financial Rules (2017).
- **MCA21 / Udyam / GSTN:** Government databases for Corporate Affairs, MSME registration, and Tax Identification.
- **PAN / CIN:** Permanent Account Number / Corporate Identification Number (Primary deterministic identity anchors).
- **PII:** Personally Identifiable Information.

---

## 2. Overall Description

### 2.1 Product Perspective
A standalone full-stack web application architected for government deployment.
- **Backend:** Python (FastAPI, NetworkX, PyMuPDF, Hashlib).
- **Frontend:** React (Vite, Tailwind CSS).
- **Integration Paths:** GSTN (via GSP ecosystem) and DigiLocker (OAuth 2.0) are production pathways. Udyam and MCA21 APIs are modeled via simulated JSON contracts due to restricted public access.

### 2.2 User Classes
- **Procurement Officer:** Reviews contradiction cascades and generates legally cited Show-Cause notices.
- **System Auditor (Vigilance):** Reviews the SHA-256 cryptographic hash chain to verify ledger integrity.

---

## 3. System Features (Functional Requirements)

### 3.1 Feature 1: Deterministic Claim Extraction
- **Description:** The system must accurately ingest and parse Tender PDFs and Bidder Certificates.
- **Requirements:**
  - Must rely primarily on native digital extraction (PyMuPDF) and targeted Regular Expressions (Regex) to ensure 100% reproducibility and mathematical immunity to adversarial prompt-injection attacks.
  - Generative AI (LLMs) must be explicitly removed from the critical extraction path to guarantee sub-10ms latency and zero API cost.
  - Non-English and flattened scanned documents must route to an OCR/Translation fallback tier (AWS Textract / Bhashini API), which is architecturally scoped for Phase 2 implementation.

### 3.2 Feature 2: Temporal Evidence Provenance Graph Engine
- **Description:** The core NetworkX evaluation engine that maps relationships between Bidders, Identity Anchors, and Evidence.
- **Requirements:**
  - **Deterministic Anchoring:** Must use PAN as the primary graph key. Fuzzy name matching is demoted strictly to a secondary "Identity Inconsistency Risk" signal and must never trigger a silent, automated merge.
  - **Temporal Compliance:** Must evaluate evidence validity strictly as of the **Tender Closing Date**, not the current system clock, closing loopholes around expired vigilance debarments.
  - **5-State Evaluation:** Must classify the compliance graph into one of five states: `VERIFIED_COMPLIANT`, `NON_COMPLIANT`, `NEEDS_REVIEW`, `UNVERIFIED`, or `NOT_APPLICABLE`.

### 3.3 Feature 3: Cross-Bidder Collusion Engine
- **Description:** A heuristic anomaly detection engine that scans across the entire bidder network for cartelization.
- **Requirements:**
  - Must cross-reference hidden signals, such as identical PDF author metadata and shared MCA21 directors.
  - Must strictly label these overlaps as "Investigative Leads" requiring officer review, never as deterministic disqualifications.

### 3.4 Feature 4: Cryptographic Audit Ledger & Statutory Action
- **Description:** A secure logging mechanism that records officer actions in a tamper-evident chain.
- **Requirements:**
  - Every officer decision (e.g., Generate Show-Cause Notice) must append to the ledger.
  - Must auto-generate statutory notice text citing applicable laws (e.g., GFR 2017 Rule 175 for misrepresentation, chained to Rule 151).
  - Must recursively scan and aggressively redact PII (specifically 12-digit Aadhaar numbers) via Regex prior to hashing to maintain strict **DPDP Act Compliance**.
  - Must link sequential events using a SHA-256 cryptographic hash to mathematically prevent retroactive database alteration by rogue administrators.

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- **Web Dashboard:** A React-based UI providing a split-screen Contradiction Cascade, prioritizing high-contrast alerts (Red/Yellow/Green) and an interactive Hub-and-Spoke Evidence Graph representation.

### 4.2 Software Interfaces
- **Mocked Integrations:** MCA21 (Directors/Financials), Udyam (MSME Classification), and Vigilance databases are simulated via local JSON contracts.
- **Target Integrations:** GSTN (GSP APIs), Bhashini (Regional Translation).

### 4.3 Key API Endpoints
- `POST /api/v1/tenders/{tender_id}/compile-rules`: Triggers Regex-based extraction of rule thresholds.
- `POST /api/v1/verify/bidder/{bidder_id}`: Executes the NetworkX temporal graph evaluation.
- `GET /api/v1/tenders/{tender_id}/collusion-signals`: Runs network-wide cartelization heuristics.
- `POST /api/v1/officer/decision`: Commits the officer's action to the SHA-256 ledger.

---

## 5. Non-Functional Requirements

### 5.1 Performance
- **Sub-10ms Latency:** The system must resolve graph traversal and contradiction detection in extremely low latency. The current in-memory NetworkX engine must maintain its verified benchmark of **~4.09ms** average per request prior to database commit.

### 5.2 Security
- **Prompt Injection Defense:** By utilizing deterministic extraction over LLMs for the critical path, the system must process adversarial prompt-injection payloads as inert strings, preventing prompt hijacking.
- **Rogue Sysadmin Defense:** The SHA-256 hash chain must ensure that internal actors with database access cannot silently delete or alter compliance records.

### 5.3 Compliance
- **Data Privacy:** PII masking is non-negotiable and must execute synchronously before any ledger commit to satisfy the DPDP Act.
