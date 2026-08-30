# Software Requirements Specification (SRS)
**Project Name:** GeM Compliance Platform (Smart India Hackathon Edition)
**Version:** 1.0

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document details the functional and non-functional requirements for the GeM (Government e Marketplace) Compliance Platform. The system is designed to automate the verification of bidder claims against authoritative government data sources, drastically reducing manual officer workload while preserving strict deterministic legal standards.

### 1.2 Scope
The platform serves as an intelligent middleware for government procurement officers. It ingests unstructured bidder documents (Tenders, CA Certificates), extracts claims using AI, and deterministically validates those claims against external authoritative APIs (MCA21, Udyam, GSTN). The system does not auto-disqualify bidders; instead, it highlights contradictions via an Evidence Provenance Graph and securely logs Officer decisions onto a tamper-evident SHA-256 ledger.

### 1.3 Definitions and Acronyms
- **GeM:** Government e Marketplace.
- **DPDP Act:** Digital Personal Data Protection Act (India).
- **GFR:** General Financial Rules (2017).
- **MCA21:** Ministry of Corporate Affairs database.
- **RAG:** Retrieval-Augmented Generation.
- **OCR:** Optical Character Recognition.
- **PII:** Personally Identifiable Information.

---

## 2. Overall Description

### 2.1 Product Perspective
The platform operates as a standalone web application consisting of a React-based frontend dashboard and a Python/FastAPI backend. It integrates hypothetically with government databases and utilizes NetworkX for in-memory graph traversals to evaluate compliance rules.

### 2.2 User Classes and Characteristics
- **Procurement Officer (Primary User):** Government official responsible for awarding tenders. Requires clear, legally defensible, and actionable insights. Not necessarily technically trained.
- **System Auditor (Secondary User):** Responsible for reviewing the cryptographic ledger to ensure no decisions were altered retroactively.

### 2.3 Operating Environment
- **Backend:** Python 3.10+, FastAPI, NetworkX.
- **Frontend:** Node.js, React 19, Vite, Tailwind CSS.
- **Database:** PostgreSQL (with `pgvector` and `pgcrypto` extensions) [Note: Simulated via in-memory structures for prototype].
- **Deployment:** Containerized via Docker, compatible with standard Linux cloud environments.

---

## 3. System Features

### 3.1 Feature 1: Evidence Provenance Graph Engine
- **Description:** The system must construct a directed graph linking a Bidder to their specific Identity Anchors (e.g., PAN), Claims (e.g., Turnover from PDF), and Evidence (e.g., Turnover from MCA21 API).
- **Functional Requirements:**
  - The engine must successfully map Claims and Evidence to a deterministic Anchor.
  - The engine must evaluate specific hardcoded limits (e.g., Micro MSME Turnover <= ₹10Cr).
  - If a Claim contradicts Authoritative Evidence, the engine must generate an `[EVIDENCE_CONFLICT]` edge.
  - The system must classify the overall bidder state into one of four categories: `VERIFIED_COMPLIANT`, `NEEDS_REVIEW`, `INVESTIGATIVE_LEAD`, or `NON_COMPLIANT`.

### 3.2 Feature 2: Contradiction Cascade UI
- **Description:** A split-screen user interface designed to rapidly surface the exact nature of a compliance failure.
- **Functional Requirements:**
  - Must display the Bidder's Claim alongside the conflicting Government Evidence.
  - Must display an AI-generated synthesis explaining the contradiction in plain language.
  - Must provide a "Generate Show-Cause Notice" action button.

### 3.3 Feature 3: Cryptographic Audit Ledger
- **Description:** A secure logging mechanism that records officer actions in a tamper-evident chain.
- **Functional Requirements:**
  - Every officer decision must be appended to the ledger.
  - The system must recursively scan and redact sensitive PII (specifically 12-digit Aadhaar numbers) from the payload prior to hashing.
  - The ledger must link sequential events using a SHA-256 cryptographic hash (`hash(previous_hash + timestamp + payload)`).
  - The system must auto-generate statutory notice text citing applicable laws (e.g., GFR 2017 Rule 175).

### 3.4 Feature 4: Cross-Bidder Collusion Engine
- **Description:** A heuristic anomaly detection engine that scans across multiple bidders within a single tender to identify cartelization.
- **Functional Requirements:**
  - Must compare all bidders within a given `tender_id`.
  - Must flag identical directors found in MCA21 records.
  - Must flag identical author metadata and creation timestamps in uploaded technical PDFs.
  - Must label these findings strictly as "Investigative Leads" with a mandatory disclaimer that they are heuristic signals, not deterministic findings.

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- **Web Dashboard:** Must be responsive, built with Tailwind CSS, prioritizing high-contrast alerts (Red/Yellow/Green) for rapid officer triage.

### 4.2 Software Interfaces (Mocked for Prototype)
- **MCA21 API:** Used for fetching corporate directors and reported financial turnover.
- **Udyam Registration API:** Used for verifying MSME status and enterprise type.
- **GSTN API:** Used to verify GST compliance and active status.
- **LLM Interface (OpenAI/Gemini):** Used to extract deterministic rules from unstructured Tender PDFs via structured JSON function calling.

### 4.3 API Endpoints
- `POST /api/v1/tenders/{tender_id}/compile-rules`: Triggers LLM extraction of clauses.
- `POST /api/v1/ingest/document`: Handles PDF uploads and OCR extraction.
- `POST /api/v1/verify/bidder/{bidder_id}/tender/{tender_id}`: Executes the NetworkX graph evaluation.
- `GET /api/v1/dashboard/bidder/{bidder_id}`: Retrieves dashboard visualization data.
- `GET /api/v1/tenders/{tender_id}/collusion-signals`: Runs the cartelization heuristics.
- `POST /api/v1/officer/decision`: Commits action to the SHA-256 ledger.

---

## 5. Non-Functional Requirements

### 5.1 Performance
- Graph traversal and contradiction detection must resolve in `< 500ms` for a standard bidder profile to ensure the UI feels instantaneous.

### 5.2 Security and Compliance
- **DPDP Act Compliance:** System must aggressively sanitize PII (Aadhaar, unmasked PANs) from logs and cryptographic ledgers.
- **Data Provenance:** The UI must never present AI-generated data as authoritative truth; it must always clearly label the source (e.g., "MCA21 API 🟡").

### 5.3 Reliability and Fallbacks
- **OCR Failure:** If PDF extraction fails or confidence is low, the system must not auto-reject. It must gracefully degrade to a manual review state.
- **API Timeout:** If an external government API fails to respond, the corresponding graph node must be marked as `UNVERIFIED`, pausing deterministic evaluation.
