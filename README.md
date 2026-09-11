# SATARK — AI-Powered GeM Compliance Verification

> **Smart India Hackathon 2026** · Government e-Marketplace (GeM) · Procurement Integrity

[![React](https://img.shields.io/badge/React-18-61dafb?logo=react)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

SATARK is an AI-powered compliance verification platform for government procurement on GeM. It automates document verification, detects fraud, flags cartelization, and gives procurement officers a single dashboard to make fast, auditable decisions.

---

## The Problem

India's Government e-Marketplace processes thousands of tenders annually. Procurement officers manually verify dozens of documents per bidder — GST certificates, Udyam registrations, CA turnover certificates, work orders, EPFO/ESIC records — entirely by hand. Fraudulent documents slip through. Cartels go undetected. The process is slow, opaque, and audit-unfriendly.

---

## What SATARK Does

### Compliance Score & Dashboard
Every bidder gets a 0–100 compliance score computed from document verifications, graph contradictions, experience validation, and technical spec matching. The dashboard updates live as documents are uploaded.

### AI Document Parsing
Upload any GeM document and SATARK extracts structured data instantly using forensic PDF analysis — no third-party OCR API needed.

| Document | Extracted Fields |
|---|---|
| GST Certificate | GSTIN, composition status, filing history |
| Udyam Registration | MSME category, investment, turnover |
| CA Turnover Certificate | Turnover (Cr), UDIN, CA name, FY |
| Work Orders | Value, client, date, execution status |
| EPFO / ESIC | Contribution status, employee count |
| NSIC Certificate | Categories, EMD exemption eligibility |

### Evidence Graph Engine
Every extracted claim is a node in a knowledge graph. Contradictions between documents are automatically surfaced — e.g. MCA-reported turnover vs CA certificate discrepancy.

### Visual Authenticity Check
Detects missing signatures and rubber stamps forensically. Unsigned documents trigger a red critical banner and a 50-point score penalty on the dashboard.

### Forgery / Identity Mismatch Detection
If a bidder uploads another company's document, SATARK detects the entity name mismatch and **blocks the compliance score** with a FORGERY ALERT.

### Anti-Cartelization Scanner
Cross-bidder analysis flags shared directors, identical bid structures, and suspiciously correlated pricing patterns.

### Batch Mode
Upload a ZIP of all bidder submissions. SATARK scores every bidder simultaneously with full compliance breakdowns.

### Officer Final Review
AI provides a recommendation. The procurement officer makes the authoritative decision. Every action is hashed and logged to an immutable audit trail.

---

## Architecture

```
Frontend (React + Vite + Tailwind)
  PDF Viewer | Compliance Dashboard | Batch Mode | Evidence Graph
       |
  FastAPI Backend (Python 3.11)
       |
  Document Parsers (PyMuPDF) | Graph Engine (NetworkX) | Collusion Engine
  Visual Auth | Batch Engine | Audit Engine
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, Zustand |
| Backend | FastAPI, Python 3.11, Uvicorn |
| PDF Analysis | PyMuPDF, ReportLab |
| Graph Engine | NetworkX |
| Deployment | Vercel (frontend) + Render (backend) |

---

## Running Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## Compliance Score

| Score | Risk | Action |
|---|---|---|
| 80-100 | LOW | Approve |
| 60-79 | MEDIUM | Clarify |
| 40-59 | HIGH | Officer Review |
| 0-39 | CRITICAL | Reject |
| BLOCKED | FORGERY | Investigate |

---

## Built At

**Smart India Hackathon 2026**

MIT License