"""
Generates a professional SRS PDF for the GeM Compliance Platform
using Playwright + Chromium (proper rendering, no font issues).
"""
import asyncio
from playwright.async_api import async_playwright

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: 'Inter', Arial, sans-serif; font-size: 10.5pt; color: #1a1a2e; background: white; line-height: 1.7; }

  /* Cover page */
  .cover { page-break-after: always; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; background: linear-gradient(135deg, #1a237e 0%, #0d47a1 60%, #01579b 100%); color: white; padding: 3cm; text-align: center; }
  .cover .org { font-size: 11pt; letter-spacing: 3px; text-transform: uppercase; opacity: 0.8; margin-bottom: 16pt; }
  .cover h1 { font-size: 26pt; font-weight: 700; line-height: 1.3; margin-bottom: 8pt; }
  .cover .subtitle { font-size: 13pt; opacity: 0.85; margin-bottom: 32pt; }
  .cover .meta-box { background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); border-radius: 10px; padding: 20pt 32pt; text-align: left; min-width: 420pt; }
  .cover .meta-row { display: flex; justify-content: space-between; padding: 5pt 0; border-bottom: 1px solid rgba(255,255,255,0.15); font-size: 9.5pt; }
  .cover .meta-row:last-child { border-bottom: none; }
  .cover .meta-label { opacity: 0.7; }
  .cover .meta-val { font-weight: 600; }
  .cover .badge { display: inline-block; margin-top: 24pt; background: #f57f17; color: white; padding: 6pt 18pt; border-radius: 20pt; font-size: 9pt; font-weight: 700; letter-spacing: 1px; }

  /* ToC */
  .toc { page-break-after: always; padding: 2cm 2.5cm; }
  .toc h2 { font-size: 18pt; color: #1a237e; border-bottom: 3px solid #1a237e; padding-bottom: 8pt; margin-bottom: 20pt; }
  .toc-section { display: flex; justify-content: space-between; padding: 5pt 0; border-bottom: 1px dotted #ccc; font-size: 10pt; }
  .toc-section .num { color: #1a237e; font-weight: 700; width: 30pt; flex-shrink: 0; }
  .toc-section .title { flex: 1; }
  .toc-section .pg { color: #888; }
  .toc-sub { padding-left: 20pt; font-size: 9.5pt; color: #444; }

  /* Content */
  .content { padding: 1.8cm 2.5cm; }
  .section { margin-bottom: 28pt; }
  h2.sec { font-size: 16pt; color: #1a237e; border-bottom: 2.5px solid #1a237e; padding-bottom: 6pt; margin-bottom: 14pt; margin-top: 28pt; }
  h3.sub { font-size: 12pt; color: #0d47a1; margin: 14pt 0 6pt 0; font-weight: 600; }
  h4.subsub { font-size: 10.5pt; color: #283593; margin: 10pt 0 4pt 0; font-weight: 600; }
  p { margin-bottom: 8pt; text-align: justify; }
  ul, ol { margin: 6pt 0 10pt 22pt; }
  li { margin-bottom: 4pt; }

  /* Tables */
  table { width: 100%; border-collapse: collapse; margin: 10pt 0 16pt 0; font-size: 9.5pt; }
  th { background: #1a237e; color: white; padding: 7pt 10pt; text-align: left; font-weight: 600; }
  td { padding: 6pt 10pt; border-bottom: 1px solid #e0e0e0; vertical-align: top; }
  tr:nth-child(even) td { background: #f5f5f5; }

  /* Badges */
  .badge-green  { display:inline-block; background:#e8f5e9; color:#2e7d32; border:1px solid #a5d6a7; border-radius:4px; padding:1pt 6pt; font-size:8.5pt; font-weight:700; }
  .badge-yellow { display:inline-block; background:#fff8e1; color:#f57f17; border:1px solid #ffe082; border-radius:4px; padding:1pt 6pt; font-size:8.5pt; font-weight:700; }
  .badge-red    { display:inline-block; background:#ffebee; color:#c62828; border:1px solid #ef9a9a; border-radius:4px; padding:1pt 6pt; font-size:8.5pt; font-weight:700; }
  .badge-blue   { display:inline-block; background:#e3f2fd; color:#1565c0; border:1px solid #90caf9; border-radius:4px; padding:1pt 6pt; font-size:8.5pt; font-weight:700; }

  /* Code block */
  .code { background:#f8f8f8; border:1px solid #ddd; border-left:3px solid #1a237e; padding:10pt 14pt; font-family:monospace; font-size:8.5pt; border-radius:3px; margin:8pt 0 12pt 0; white-space:pre-wrap; }

  /* Info box */
  .infobox { background:#e3f2fd; border-left:4px solid #1565c0; padding:10pt 14pt; border-radius:3px; margin:10pt 0; font-size:9.5pt; }
  .warnbox  { background:#fff8e1; border-left:4px solid #f57f17; padding:10pt 14pt; border-radius:3px; margin:10pt 0; font-size:9.5pt; }

  /* Page break */
  .pagebreak { page-break-before: always; }

  /* Footer line */
  .footer-line { margin-top: 30pt; border-top: 1px solid #e0e0e0; padding-top: 8pt; font-size: 8pt; color: #aaa; display: flex; justify-content: space-between; }
</style>
</head>
<body>

<!-- ══════════════════════════════════════════════ COVER ══ -->
<div class="cover">
  <div class="org">Smart India Hackathon 2026 — PS 26100</div>
  <h1>GeM AI Compliance Platform</h1>
  <div class="subtitle">Software Requirements Specification (SRS)</div>
  <div class="meta-box">
    <div class="meta-row"><span class="meta-label">Document Type</span><span class="meta-val">Software Requirements Specification</span></div>
    <div class="meta-row"><span class="meta-label">Version</span><span class="meta-val">1.0 — September 2026</span></div>
    <div class="meta-row"><span class="meta-label">Problem Statement</span><span class="meta-val">PS 26100 — CPCL / MoPNG</span></div>
    <div class="meta-row"><span class="meta-label">Organization</span><span class="meta-val">Chennai Petroleum Corporation Limited (CPCL)</span></div>
    <div class="meta-row"><span class="meta-label">Ministry</span><span class="meta-val">Ministry of Petroleum &amp; Natural Gas</span></div>
    <div class="meta-row"><span class="meta-label">Status</span><span class="meta-val">✓ Implemented &amp; Live</span></div>
  </div>
  <div class="badge">AI-Powered · Zero-LLM · Graph-Based · Auditable</div>
</div>

<!-- ══════════════════════════════════════════════ ToC ══ -->
<div class="toc">
  <h2>Table of Contents</h2>
  <div class="toc-section"><span class="num">1</span><span class="title">Introduction</span><span class="pg">3</span></div>
  <div class="toc-section toc-sub"><span class="num">1.1</span><span class="title">Purpose</span></div>
  <div class="toc-section toc-sub"><span class="num">1.2</span><span class="title">Scope</span></div>
  <div class="toc-section toc-sub"><span class="num">1.3</span><span class="title">Problem Context (CPCL / PS 26100)</span></div>
  <div class="toc-section toc-sub"><span class="num">1.4</span><span class="title">Definitions &amp; Abbreviations</span></div>
  <div class="toc-section"><span class="num">2</span><span class="title">Overall System Description</span><span class="pg">4</span></div>
  <div class="toc-section toc-sub"><span class="num">2.1</span><span class="title">System Architecture</span></div>
  <div class="toc-section toc-sub"><span class="num">2.2</span><span class="title">Technology Stack</span></div>
  <div class="toc-section toc-sub"><span class="num">2.3</span><span class="title">User Roles</span></div>
  <div class="toc-section"><span class="num">3</span><span class="title">Functional Requirements</span><span class="pg">5</span></div>
  <div class="toc-section toc-sub"><span class="num">3.1</span><span class="title">FR-01: Tender Rule Extraction</span></div>
  <div class="toc-section toc-sub"><span class="num">3.2</span><span class="title">FR-02: Bidder Document Verification</span></div>
  <div class="toc-section toc-sub"><span class="num">3.3</span><span class="title">FR-03: GST Certificate Parsing</span></div>
  <div class="toc-section toc-sub"><span class="num">3.4</span><span class="title">FR-04: Udyam Certificate Parsing</span></div>
  <div class="toc-section toc-sub"><span class="num">3.5</span><span class="title">FR-05: Evidence Graph Engine</span></div>
  <div class="toc-section toc-sub"><span class="num">3.6</span><span class="title">FR-06: Compliance Dashboard</span></div>
  <div class="toc-section toc-sub"><span class="num">3.7</span><span class="title">FR-07: Contradiction Detection &amp; Review</span></div>
  <div class="toc-section toc-sub"><span class="num">3.8</span><span class="title">FR-08: Anti-Cartel / Collusion Detection</span></div>
  <div class="toc-section toc-sub"><span class="num">3.9</span><span class="title">FR-09: Regional Language Tender (Bhashini)</span></div>
  <div class="toc-section toc-sub"><span class="num">3.10</span><span class="title">FR-10: SHA-256 Audit Trail</span></div>
  <div class="toc-section toc-sub"><span class="num">3.11</span><span class="title">FR-11: PDF Viewer &amp; Tab Navigation</span></div>
  <div class="toc-section"><span class="num">4</span><span class="title">REST API Specification</span><span class="pg">8</span></div>
  <div class="toc-section"><span class="num">5</span><span class="title">Data Requirements</span><span class="pg">9</span></div>
  <div class="toc-section"><span class="num">6</span><span class="title">UI / UX Requirements</span><span class="pg">10</span></div>
  <div class="toc-section"><span class="num">7</span><span class="title">Non-Functional Requirements</span><span class="pg">11</span></div>
  <div class="toc-section"><span class="num">8</span><span class="title">PS 26100 Compliance Matrix</span><span class="pg">12</span></div>
  <div class="toc-section"><span class="num">9</span><span class="title">Limitations &amp; Future Scope</span><span class="pg">13</span></div>
</div>

<!-- ══════════════════════════════════════════════ SECTION 1 ══ -->
<div class="content">

<h2 class="sec">1. Introduction</h2>

<h3 class="sub">1.1 Purpose</h3>
<p>This Software Requirements Specification (SRS) documents all functional and non-functional requirements of the <strong>GeM AI Compliance Platform</strong> — an AI-powered, integrated bid compliance verification system developed for Smart India Hackathon 2026, Problem Statement PS 26100, submitted by Chennai Petroleum Corporation Limited (CPCL) under the Ministry of Petroleum &amp; Natural Gas.</p>
<p>The document serves as the authoritative reference for the implemented system, covering all features live at <code>http://localhost:5173</code> backed by a FastAPI server at <code>http://localhost:8000</code>.</p>

<h3 class="sub">1.2 Scope</h3>
<p>The platform automates GeM procurement bid compliance verification by:</p>
<ul>
  <li>Extracting eligibility rules from tender PDFs using AI/OCR</li>
  <li>Parsing and verifying GST, Udyam, and bidder documents via OCR</li>
  <li>Running a directed evidence graph engine to detect contradictions and fraud</li>
  <li>Providing a real-time compliance dashboard with risk scores</li>
  <li>Detecting cross-bidder cartelization via Jaccard similarity</li>
  <li>Supporting regional language tender documents via Bhashini (MeitY AI)</li>
  <li>Maintaining a SHA-256 tamper-evident audit trail</li>
</ul>

<h3 class="sub">1.3 Problem Context (CPCL / PS 26100)</h3>
<p>CPCL processes large-capital procurement tenders involving 50–200 bidders per tender, each submitting 10–15 statutory documents. Procurement officers manually cross-check information across 10+ government portals (GSTN, MCA21, Udyam, DigiLocker, etc.), resulting in:</p>
<ul>
  <li><strong>250+ officer-days per tender</strong> wasted on manual verification</li>
  <li>Inconsistencies and human errors in cross-portal checks</li>
  <li>Inability to detect document fraud (e.g., inflated turnover claims)</li>
  <li>No audit trail defensible in legal proceedings</li>
  <li>No machine-readable processing of regional language tenders</li>
</ul>

<h3 class="sub">1.4 Definitions &amp; Abbreviations</h3>
<table>
  <tr><th>Term</th><th>Definition</th></tr>
  <tr><td>GeM</td><td>Government e-Marketplace — India's national procurement portal</td></tr>
  <tr><td>CPCL</td><td>Chennai Petroleum Corporation Limited</td></tr>
  <tr><td>OCR</td><td>Optical Character Recognition — text extraction from PDFs</td></tr>
  <tr><td>SBD</td><td>Standard Bid Document</td></tr>
  <tr><td>MSME</td><td>Micro, Small and Medium Enterprise</td></tr>
  <tr><td>MII</td><td>Make in India — local content mandate</td></tr>
  <tr><td>EMD</td><td>Earnest Money Deposit</td></tr>
  <tr><td>GFR</td><td>General Financial Rules 2017</td></tr>
  <tr><td>GSTIN</td><td>GST Identification Number (15-character alphanumeric)</td></tr>
  <tr><td>Bhashini</td><td>MeitY's national language translation AI platform</td></tr>
  <tr><td>NIC</td><td>National Industrial Classification code</td></tr>
  <tr><td>SHA-256</td><td>Secure Hash Algorithm — 256-bit cryptographic hash</td></tr>
</table>

<!-- ══ SECTION 2 ══ -->
<h2 class="sec pagebreak">2. Overall System Description</h2>

<h3 class="sub">2.1 System Architecture</h3>
<p>The system follows a <strong>two-tier client-server architecture</strong> with a React SPA frontend and a FastAPI asynchronous backend, connected via REST APIs over localhost.</p>

<div class="code">┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (React 18 SPA)                   │
│  Dashboard  │  PDF Viewer  │  Evidence Graph  │  GovDocPanel│
│  Zustand Global Store (tenderRules, gstResult, udyamResult) │
└───────────────────────┬────────────────────────────────────┘
                        │ REST API (HTTP/JSON)
┌───────────────────────▼────────────────────────────────────┐
│                  FastAPI + Uvicorn (Port 8000)              │
│  rule_compiler.py │ graph_engine.py │ bhashini_integration  │
│  audit_engine.py  │ collusion_engine.py │ config.py bridge  │
└───────────────────────┬────────────────────────────────────┘
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   PyMuPDF OCR    NetworkX Graph    mock_dataset.json
   (PDF parsing)  (contradiction)   (5 bidder profiles)</div>

<h3 class="sub">2.2 Technology Stack</h3>
<table>
  <tr><th>Layer</th><th>Technology</th><th>Version</th><th>Purpose</th></tr>
  <tr><td>Frontend Framework</td><td>React</td><td>18</td><td>Component-based SPA UI</td></tr>
  <tr><td>Build Tool</td><td>Vite</td><td>5.x</td><td>HMR + fast bundling</td></tr>
  <tr><td>Styling</td><td>Tailwind CSS</td><td>3.x</td><td>Utility-first responsive design</td></tr>
  <tr><td>State Management</td><td>Zustand</td><td>4.x</td><td>Lightweight global state store</td></tr>
  <tr><td>Graph Visualization</td><td>ReactFlow</td><td>11.x</td><td>Interactive evidence provenance graph</td></tr>
  <tr><td>Scroll Physics</td><td>Lenis</td><td>1.x</td><td>Inertia smooth scroll on dashboard</td></tr>
  <tr><td>Backend Framework</td><td>FastAPI</td><td>0.111</td><td>Async REST API, auto Swagger docs</td></tr>
  <tr><td>ASGI Server</td><td>Uvicorn</td><td>0.30</td><td>Production-grade async server</td></tr>
  <tr><td>PDF OCR</td><td>PyMuPDF (fitz)</td><td>1.24</td><td>Text extraction from all PDFs</td></tr>
  <tr><td>Graph Analytics</td><td>NetworkX</td><td>3.x</td><td>Directed evidence-claim-contradiction graph</td></tr>
  <tr><td>Regional Language AI</td><td>Bhashini (MeitY)</td><td>ULCA API</td><td>OCR + translation for regional tenders</td></tr>
  <tr><td>Audit Hashing</td><td>hashlib SHA-256</td><td>stdlib</td><td>Tamper-evident audit entries</td></tr>
  <tr><td>Demo PDF Generation</td><td>ReportLab + Playwright</td><td>4.x / 1.x</td><td>GST, Udyam, Telugu tender demo PDFs</td></tr>
</table>

<h3 class="sub">2.3 User Roles</h3>
<table>
  <tr><th>Role</th><th>Actions Permitted</th></tr>
  <tr><td><strong>Procurement Officer</strong></td><td>View dashboard, upload documents, trigger verification, review contradictions, generate show-cause notices, dismiss findings</td></tr>
  <tr><td><strong>System (Automated)</strong></td><td>OCR extraction, graph construction, contradiction detection, score computation, audit logging</td></tr>
  <tr><td><strong>Bidder</strong> (future)</td><td>Upload documents via portal (not yet implemented)</td></tr>
</table>

<!-- ══ SECTION 3 ══ -->
<h2 class="sec pagebreak">3. Functional Requirements</h2>

<h3 class="sub">FR-01: Tender Rule Extraction</h3>
<h4 class="subsub">Description</h4>
<p>The system shall accept an English-language tender PDF, extract all eligibility thresholds using OCR + regex, and make them available to the verification engine and dashboard in real-time.</p>
<h4 class="subsub">Inputs / Outputs</h4>
<table>
  <tr><th>Input</th><th>Process</th><th>Output</th></tr>
  <tr><td>Tender PDF (English)</td><td>PyMuPDF text extraction → DOTALL regex named capture groups</td><td>JSON array of extracted rules + updated config.active_tender_limits</td></tr>
</table>
<h4 class="subsub">Extracted Fields</h4>
<ul>
  <li>MSME turnover limit (₹ Cr)</li>
  <li>Sub-contracting cap (%)</li>
  <li>Make in India local content minimum (%)</li>
  <li>EMD exemption status for MSEs</li>
  <li>GST compliance period (months)</li>
  <li>Debarment prohibition clause</li>
</ul>
<h4 class="subsub">Acceptance Criteria</h4>
<ul>
  <li>Each extracted rule has: clause name, description, mapped_regulatory_id (UUID)</li>
  <li>config.active_tender_limits updated within the same request</li>
  <li>Dashboard auto-refreshes (tenderRules in useEffect dependency array)</li>
  <li>Response time &lt; 500ms for PDFs up to 10MB</li>
</ul>

<h3 class="sub">FR-02: Bidder Document Verification</h3>
<h4 class="subsub">Description</h4>
<p>The system shall accept a bidder's technical bid PDF, extract all compliance claims using OCR, run those claims through the Evidence Graph Engine, and return a structured verification result.</p>
<h4 class="subsub">Extracted Fields</h4>
<ul>
  <li>turnover_cr (annual audited turnover in crores)</li>
  <li>local_content_pct (Make in India %)</li>
  <li>subcontracting_pct (sub-contracting %)</li>
  <li>pan (PAN number — 10-char alphanumeric)</li>
  <li>gst_months_missed (GST filing gap count)</li>
</ul>
<h4 class="subsub">Acceptance Criteria</h4>
<ul>
  <li>PDF displayed in iframe immediately upon upload (before API response)</li>
  <li>Blue banner "Showing results from uploaded document" shown on dashboard</li>
  <li>"✕ Clear &amp; return to dropdown" button clears upload state</li>
  <li>Graph engine runs contradiction detection against active_tender_limits</li>
</ul>

<h3 class="sub">FR-03: GST Certificate Parsing</h3>
<h4 class="subsub">Description</h4>
<p>The system shall parse a GST Registration Certificate (Form GST REG-06) PDF and extract all registration fields, flagging ineligibility conditions.</p>
<h4 class="subsub">Extracted Fields &amp; Flags</h4>
<table>
  <tr><th>Field</th><th>Type</th><th>Flag Logic</th></tr>
  <tr><td>GSTIN</td><td>15-char string</td><td>gstin_valid_format: regex [0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}</td></tr>
  <tr><td>Legal Name</td><td>string</td><td>—</td></tr>
  <tr><td>Constitution</td><td>enum</td><td>—</td></tr>
  <tr><td>Registration Date</td><td>date</td><td>—</td></tr>
  <tr><td>Registration Type</td><td>enum</td><td>composition_fail = true if type == "Composition"</td></tr>
  <tr><td>is_regular_taxpayer</td><td>boolean</td><td>false if Composition/Casual/Non-Resident</td></tr>
</table>
<h4 class="subsub">UI Rendering (GovDocPanel)</h4>
<ul>
  <li>PASS badge (green) — GSTIN valid, regular taxpayer</li>
  <li>FAIL badge (red) — Composition dealer detected</li>
  <li>Red alert banner: "⚠ Composition Dealer — Ineligible for B2G Government Procurement"</li>
</ul>

<h3 class="sub">FR-04: Udyam Certificate Parsing</h3>
<h4 class="subsub">Description</h4>
<p>The system shall parse a Udyam Registration Certificate PDF and extract enterprise classification, flagging MSME class mismatches.</p>
<h4 class="subsub">Extracted Fields &amp; Flags</h4>
<table>
  <tr><th>Field</th><th>Type</th><th>Flag Logic</th></tr>
  <tr><td>Udyam Number</td><td>UDYAM-XX-XX-XXXXXXX</td><td>udyam_number_found boolean</td></tr>
  <tr><td>Enterprise Name</td><td>string</td><td>—</td></tr>
  <tr><td>Enterprise Classification</td><td>MICRO / SMALL / MEDIUM</td><td>is_micro = false if SMALL or MEDIUM</td></tr>
  <tr><td>NIC Code + Description</td><td>string</td><td>—</td></tr>
  <tr><td>State</td><td>string</td><td>—</td></tr>
  <tr><td>Registration Date</td><td>date</td><td>—</td></tr>
</table>
<h4 class="subsub">UI Rendering (GovDocPanel)</h4>
<ul>
  <li>PASS (green) — MICRO classification confirmed</li>
  <li>FAIL (red) — SMALL or MEDIUM classification while claiming MICRO EMD exemption</li>
  <li>Red alert banner: "⚠ Enterprise is SMALL — Cannot claim MICRO EMD exemption"</li>
</ul>

<h3 class="sub">FR-05: Evidence Graph Engine</h3>
<h4 class="subsub">Description</h4>
<p>The system shall maintain a directed graph of all bidder claims, supporting evidence, and tender rule anchors. Contradictions between claims and evidence shall be represented as animated red EVIDENCE_CONFLICT edges.</p>
<h4 class="subsub">Node Types</h4>
<table>
  <tr><th>Node Type</th><th>Color</th><th>Example</th></tr>
  <tr><td>Bidder</td><td>Black</td><td>"ACME Corp (bidder-acme-001)"</td></tr>
  <tr><td>Claim</td><td>Pink</td><td>"Claimed Turnover: ₹8.5 Cr"</td></tr>
  <tr><td>Evidence</td><td>Green</td><td>"MCA21: Actual Turnover ₹14.5 Cr"</td></tr>
  <tr><td>Anchor:TenderRule</td><td>Purple</td><td>"MSME Turnover ≤ ₹10 Cr"</td></tr>
</table>
<h4 class="subsub">Edge Types</h4>
<table>
  <tr><th>Edge</th><th>Meaning</th><th>Style</th></tr>
  <tr><td>MAKES_CLAIM</td><td>Bidder → Claim</td><td>Solid grey</td></tr>
  <tr><td>VERIFIED_AGAINST</td><td>Claim → Evidence</td><td>Solid blue</td></tr>
  <tr><td>EVIDENCE_CONFLICT</td><td>Evidence → Claim</td><td>Animated red dashed</td></tr>
  <tr><td>ANCHORED_TO</td><td>Claim → TenderRule</td><td>Solid purple</td></tr>
</table>
<h4 class="subsub">Contradiction Scenarios Detected</h4>
<ol>
  <li><strong>MCA21 Turnover Mismatch</strong> — Bidder claimed &lt; actual MCA21 turnover</li>
  <li><strong>MII Local Content Shortfall</strong> — local_content_pct &lt; active_tender_limits["mii"]</li>
  <li><strong>Sub-contracting Breach</strong> — subcontracting_pct &gt; active_tender_limits["subcontract"]</li>
  <li><strong>GST Filing Gap</strong> — gst_months_missed &gt; 0</li>
  <li><strong>Time-Travel Fraud</strong> — GST filing date before company incorporation date</li>
  <li><strong>Debarment Active</strong> — debarred = true in bidder record</li>
</ol>

<h3 class="sub">FR-06: Compliance Dashboard</h3>
<h4 class="subsub">Description</h4>
<p>The system shall display a real-time compliance dashboard for any selected bidder, showing all verification results in a single unified view.</p>
<h4 class="subsub">Dashboard Components</h4>
<table>
  <tr><th>Component</th><th>Description</th></tr>
  <tr><td>Bidder Selector Dropdown</td><td>5 demo bidder profiles — selection triggers auto-verification</td></tr>
  <tr><td>Hard Filter Row</td><td>PAN Active / GST Active / Not Debarred — instant PASS/FAIL</td></tr>
  <tr><td>Compliance Score</td><td>0–100 numeric score with colour-coded risk level</td></tr>
  <tr><td>Risk Badge</td><td>LOW / MEDIUM / HIGH / CRITICAL based on score thresholds</td></tr>
  <tr><td>Evidence Graph</td><td>ReactFlow interactive graph — column layout, zoom, pan</td></tr>
  <tr><td>GovDocPanel</td><td>GST + Udyam OCR results — field-level PASS/WARN/FAIL badges</td></tr>
  <tr><td>Contradiction Panel</td><td>All CONFLICT edges listed as actionable cards</td></tr>
  <tr><td>Audit Log</td><td>SHA-256 hash per action — timestamped, tamper-evident</td></tr>
</table>

<h3 class="sub">FR-07: Contradiction Detection &amp; Review</h3>
<h4 class="subsub">Description</h4>
<p>Each detected contradiction shall be surfaced as an actionable card with two officer actions.</p>
<table>
  <tr><th>Action</th><th>Effect</th></tr>
  <tr><td>Dismiss Finding</td><td>Removes contradiction card; logs "DISMISSED" audit entry with SHA-256</td></tr>
  <tr><td>Show-Cause Notice</td><td>Generates formatted notice text; logs "SHOW_CAUSE_ISSUED" audit entry</td></tr>
</table>

<h3 class="sub">FR-08: Anti-Cartel / Collusion Detection</h3>
<h4 class="subsub">Description</h4>
<p>The system shall scan all bidders in a tender for cartelization signals using cross-bidder analysis.</p>
<h4 class="subsub">Detection Methods</h4>
<ul>
  <li><strong>Jaccard Similarity</strong> — similarity of claimed values across bidders (turnover, local content, subcontracting)</li>
  <li><strong>Shared NIC Code</strong> — multiple bidders with identical NIC codes flagged</li>
  <li><strong>Sub-contracting Ring</strong> — bidder A subs to B who subs to A pattern</li>
</ul>
<div class="warnbox">Legal guardrail: All collusion signals are presented with disclaimer — "Investigative Lead Only. Final qualification decision rests with Procurement Officer."</div>

<h3 class="sub">FR-09: Regional Language Tender — Bhashini Pipeline</h3>
<h4 class="subsub">Description</h4>
<p>The system shall accept tender documents in Indian regional languages, translate them to English via Bhashini (MeitY AI), and extract compliance rules from the translated text.</p>
<h4 class="subsub">Supported Languages</h4>
<p>Telugu (te), Malayalam (ml), Hindi (hi), Tamil (ta), Kannada (kn), Bengali (bn)</p>
<h4 class="subsub">Processing Pipeline</h4>
<ol>
  <li>Upload regional PDF to Tender Document tab in PDF viewer</li>
  <li>Click "🇮🇳 Bhashini Translate" button (only visible on Tender tab)</li>
  <li>Select source language from dropdown</li>
  <li>POST /api/v1/tenders/translate-regional</li>
  <li>PyMuPDF tries text extraction — if text layer exists → use directly</li>
  <li>If scanned image PDF (&lt;50 chars) → Bhashini OCR + Translation API</li>
  <li>Rule compiler extracts compliance thresholds from resulting text</li>
  <li>Dashboard shows: translation source badge, preview, rules extracted count</li>
</ol>
<h4 class="subsub">Translation Source Badges</h4>
<ul>
  <li><span class="badge-green">✓ BHASHINI API</span> — live Bhashini ULCA API used (BHASHINI_TOKEN set)</li>
  <li><span class="badge-yellow">⚠ SIMULATION MODE</span> — no token; sandbox simulation</li>
  <li><span class="badge-blue">PDF_TEXT_EXTRACTED</span> — text-layer PDF; OCR not needed</li>
</ul>

<h3 class="sub">FR-10: SHA-256 Audit Trail</h3>
<h4 class="subsub">Description</h4>
<p>Every officer action shall produce a tamper-evident audit entry containing a SHA-256 hash of the action data.</p>
<h4 class="subsub">Audit Entry Schema</h4>
<div class="code">{
  "timestamp":   "2026-09-06T14:23:11Z",
  "action":      "SHOW_CAUSE_ISSUED | DISMISSED | VERIFIED | UPLOADED",
  "bidder_id":   "bidder-delta-004",
  "officer_id":  "officer-001",
  "payload":     { ... action-specific data ... },
  "sha256_hash": "a3f9b2c1d4e8f7a6b5c4d3e2f1a0b9c8..."
}</div>
<h4 class="subsub">Acceptance Criteria</h4>
<ul>
  <li>Hash computed over: timestamp + action + bidder_id + officer_id + payload JSON</li>
  <li>Audit log displayed on dashboard — most recent entry at top</li>
  <li>Entries are append-only (no delete endpoint)</li>
</ul>

<h3 class="sub">FR-11: PDF Viewer &amp; Tab Navigation</h3>
<h4 class="subsub">Description</h4>
<p>The right panel shall contain a resizable PDF viewer with three document tabs, each with context-aware upload buttons.</p>
<table>
  <tr><th>Tab</th><th>Default PDF</th><th>Upload Button</th><th>Color</th><th>Backend Endpoint</th></tr>
  <tr><td>Tender Document</td><td>tender_demo.pdf</td><td>Upload Bidder Document + 🇮🇳 Bhashini</td><td>Grey</td><td>/verify-document</td></tr>
  <tr><td>GST Certificate</td><td>gst_tender_demo.pdf</td><td>Upload GST Certificate</td><td>Orange</td><td>/parse-gst</td></tr>
  <tr><td>Udyam Certificate</td><td>udyam_tender_demo.pdf</td><td>Upload Udyam Certificate</td><td>Green</td><td>/parse-udyam</td></tr>
</table>

<!-- ══ SECTION 4 ══ -->
<h2 class="sec pagebreak">4. REST API Specification</h2>

<table>
  <tr><th>Method</th><th>Endpoint</th><th>Description</th><th>Key Response Fields</th></tr>
  <tr><td>POST</td><td>/api/v1/tenders/{id}/compile-rules</td><td>OCR tender PDF → extract rules → update config</td><td>extracted_rules[], tender_id</td></tr>
  <tr><td>POST</td><td>/api/v1/verify/bidder/{bid}/tender/{tid}</td><td>Run graph engine on mock dataset bidder</td><td>compliance_score, risk_level, contradictions[]</td></tr>
  <tr><td>GET</td><td>/api/v1/dashboard/bidder/{id}</td><td>Return serialized graph + score + contradictions</td><td>nodes[], edges[], score, risk_level</td></tr>
  <tr><td>POST</td><td>/api/v1/bidders/verify-document</td><td>OCR bidder tech bid PDF → graph engine</td><td>extracted_claims, compliance_score, contradictions[]</td></tr>
  <tr><td>POST</td><td>/api/v1/bidders/parse-gst</td><td>OCR GST REG-06 PDF → extract fields + flags</td><td>gstin, registration_type, composition_fail</td></tr>
  <tr><td>POST</td><td>/api/v1/bidders/parse-udyam</td><td>OCR Udyam cert PDF → extract fields + flags</td><td>udyam_number, enterprise_classification, is_micro</td></tr>
  <tr><td>POST</td><td>/api/v1/tenders/translate-regional</td><td>PyMuPDF / Bhashini pipeline for regional PDF</td><td>translation_source, translated_text_preview, rule_count</td></tr>
  <tr><td>GET</td><td>/api/v1/tenders/{id}/collusion-signals</td><td>Jaccard cross-bidder cartelization scan</td><td>signals[], similarity_scores</td></tr>
  <tr><td>POST</td><td>/api/v1/audit/log</td><td>Append SHA-256 audit entry</td><td>entry_id, sha256_hash, timestamp</td></tr>
</table>

<!-- ══ SECTION 5 ══ -->
<h2 class="sec">5. Data Requirements</h2>

<h3 class="sub">5.1 Demo Bidder Profiles (mock_dataset.json)</h3>
<table>
  <tr><th>Bidder ID</th><th>Scenario</th><th>Embedded Violation</th><th>Expected Outcome</th></tr>
  <tr><td>bidder-acme-001</td><td>✅ Compliant baseline</td><td>None</td><td>Score: 92, Risk: LOW</td></tr>
  <tr><td>bidder-delta-004</td><td>❌ MCA21 turnover fraud</td><td>Claimed ₹8.5 Cr, MCA21 says ₹14.5 Cr</td><td>Score: 45, Risk: HIGH + CONFLICT</td></tr>
  <tr><td>bidder-theta-007</td><td>❌ Time-travel fraud</td><td>GST filed before company registration</td><td>Score: 20, Risk: CRITICAL</td></tr>
  <tr><td>bidder-echo-005</td><td>❌ Multi-rule breach</td><td>MII 30% + Sub 45% + GST 6mo gap</td><td>Score: 15, Risk: CRITICAL</td></tr>
  <tr><td>bidder-foxtrot-006</td><td>⚠️ Partial fail</td><td>MII 35% + GST 3mo missed</td><td>Score: 58, Risk: MEDIUM</td></tr>
</table>

<h3 class="sub">5.2 Demo Government Document PDFs</h3>
<table>
  <tr><th>File</th><th>Type</th><th>Deliberate Violation</th></tr>
  <tr><td>gst_tender_demo.pdf</td><td>GST REG-06</td><td>Registration Type: Composition (B2G ineligible)</td></tr>
  <tr><td>udyam_tender_demo.pdf</td><td>Udyam Certificate</td><td>Classification: SMALL (claiming MICRO benefits)</td></tr>
  <tr><td>bidder_foxtrot.pdf</td><td>Bidder Tech Bid</td><td>Local Content 35% + GST 3-month gap</td></tr>
  <tr><td>telugu_tender_demo.pdf</td><td>Telugu Tender (Playwright)</td><td>All 6 rules in Telugu — for Bhashini pipeline testing</td></tr>
</table>

<h3 class="sub">5.3 Zustand Store Schema</h3>
<div class="code">// dashboardStore.js — all global state slices
{
  selectedDocument:     'tender' | 'gst' | 'udyam',
  tenderRules:          RuleObject[],          // dynamically extracted
  verifiedDocResult:    VerificationResult | null,
  gstParseResult:       GstParseResult | null,
  udyamParseResult:     UdyamParseResult | null,
  auditLog:             AuditEntry[],          // SHA-256 entries
  viewerRef:            { goToPage(n: number): void } | null,

  // Actions
  setTenderRules, setVerifiedDocResult, clearVerifiedDocResult,
  setGstParseResult, clearGstParseResult,
  setUdyamParseResult, clearUdyamParseResult,
  addAuditEntry, setViewerRef
}</div>

<!-- ══ SECTION 6 ══ -->
<h2 class="sec pagebreak">6. UI / UX Requirements</h2>

<table>
  <tr><th>Feature</th><th>Requirement</th><th>Implementation</th></tr>
  <tr><td>Resizable Split Panel</td><td>Drag divider left/right to resize PDF vs Dashboard panels</td><td>mousemove on window, getBoundingClientRect, empty [] deps (no stale closure)</td></tr>
  <tr><td>Iframe Drag Shield</td><td>Mouse events must not be stolen by PDF iframe during drag</td><td>position:absolute; inset:0; z-index:50 overlay during isDragging</td></tr>
  <tr><td>Minimize PDF Panel</td><td>Officer can hide PDF panel to expand dashboard view</td><td>Width → 0 with CSS transition; only when !isDragging</td></tr>
  <tr><td>Lenis Smooth Scroll</td><td>Dashboard scrolls with physics inertia</td><td>new Lenis({ wrapper: rightPanelRef }) + rAF loop</td></tr>
  <tr><td>Context-aware Upload</td><td>Button label + color matches current document tab</td><td>UPLOAD_CONFIG map: tab → endpoint + field + color classes</td></tr>
  <tr><td>ReactFlow Graph Layout</td><td>Columns: Bidder x=0, Claims x=250, Evidence x=560, Anchors x=870</td><td>EvidenceGraph.jsx column auto-layout algorithm</td></tr>
  <tr><td>Animated Conflict Edges</td><td>Red dashed animated edges on EVIDENCE_CONFLICT connections</td><td>animated:true, style:{stroke:'#ef4444'} on edge</td></tr>
  <tr><td>Anti-cartel Modal</td><td>Full-screen modal with legal guardrail disclaimer</td><td>App.jsx modal state + Jaccard results table</td></tr>
  <tr><td>Responsive Layout</td><td>Works on 1280px+ screens</td><td>Tailwind flex/grid — not mobile-optimized (procurement officer use case)</td></tr>
</table>

<!-- ══ SECTION 7 ══ -->
<h2 class="sec">7. Non-Functional Requirements</h2>

<table>
  <tr><th>Category</th><th>Requirement</th><th>Target</th></tr>
  <tr><td>Performance</td><td>OCR + graph verification latency</td><td>&lt; 500ms per bidder</td></tr>
  <tr><td>Performance</td><td>Dashboard initial load time</td><td>&lt; 2s (Vite bundled)</td></tr>
  <tr><td>Reliability</td><td>Backend uptime during demo</td><td>Uvicorn restart &lt; 5s</td></tr>
  <tr><td>Security</td><td>Audit entries</td><td>SHA-256 hash — tamper-evident</td></tr>
  <tr><td>Accuracy</td><td>GSTIN regex validation</td><td>15-char pattern [0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]</td></tr>
  <tr><td>Accuracy</td><td>Udyam number regex</td><td>UDYAM-[A-Z]{2}-[0-9]{2}-[0-9]{7}</td></tr>
  <tr><td>Scalability</td><td>Mock dataset bidders</td><td>5 profiles — architecture supports N via JSON extension</td></tr>
  <tr><td>Maintainability</td><td>Config bridge</td><td>config.active_tender_limits — single source of truth for all thresholds</td></tr>
  <tr><td>Compliance</td><td>Officer autonomy</td><td>System is decision-support only — final qualification decision with officer (GFR 2017)</td></tr>
  <tr><td>Transparency</td><td>AI explainability</td><td>All decisions backed by evidence nodes — no black-box scoring</td></tr>
</table>

<!-- ══ SECTION 8 ══ -->
<h2 class="sec pagebreak">8. PS 26100 Compliance Matrix</h2>

<table>
  <tr><th>PS 26100 Expected Capability</th><th>Our Implementation</th><th>Status</th></tr>
  <tr><td>1. Integrate with Government portals/databases</td><td>GST OCR + Udyam OCR + MCA21 mock dataset</td><td><span class="badge-yellow">PARTIAL</span></td></tr>
  <tr><td>2. Verify Udyam/MSME status</td><td>parse-udyam endpoint — full OCR parse + is_micro flag</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>3. Verify GST registration and return filing</td><td>parse-gst endpoint — GSTIN, type, composition flag</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>4. Verify PAN and Income Tax compliance</td><td>PAN hard filter in graph engine (mock)</td><td><span class="badge-yellow">PARTIAL</span></td></tr>
  <tr><td>5. Check Make in India local content</td><td>MII % extracted from tender + graph contradiction</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>6. Verify EPFO/ESIC compliance</td><td>Not implemented</td><td><span class="badge-red">GAP</span></td></tr>
  <tr><td>7. Startup India / NSIC / OEM authorization</td><td>Not implemented</td><td><span class="badge-red">GAP</span></td></tr>
  <tr><td>8. DigiLocker / document verification</td><td>Mock only — architecture supports OAuth plug-in</td><td><span class="badge-yellow">PARTIAL</span></td></tr>
  <tr><td>9. Blacklisting and debarment status</td><td>Debarment hard filter in graph engine</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>10. Tender-specific compliance checks</td><td>Dynamic rule extraction → config bridge → graph engine</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>11. AI to identify missing/inconsistent information</td><td>Evidence graph CONFLICT edges + contradiction panel</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>12. Compliance Score and Risk Level</td><td>0–100 score + LOW/MEDIUM/HIGH/CRITICAL badge</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>13. AI-generated recommendation to officer</td><td>Contradiction cards + Show-Cause Notice generation</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>14. Auditable record of verification</td><td>SHA-256 tamper-evident audit trail + log UI</td><td><span class="badge-green">FULL</span></td></tr>
  <tr><td>BONUS: Regional language tenders</td><td>Bhashini MeitY AI pipeline (Telugu/Malayalam/Hindi…)</td><td><span class="badge-green">IMPLEMENTED</span></td></tr>
  <tr><td>BONUS: Anti-cartel detection</td><td>Jaccard cross-bidder collusion scan</td><td><span class="badge-green">IMPLEMENTED</span></td></tr>
</table>

<div class="infobox">
  <strong>Coverage Summary:</strong> 9 of 14 PS requirements fully implemented (64%), 3 partial (21%), 2 gaps (EPFO/ESIC + Startup India — require government API credentials outside SIH scope). Plus 2 bonus features not required by PS: Bhashini regional language and anti-cartel detection.
</div>

<!-- ══ SECTION 9 ══ -->
<h2 class="sec">9. Limitations &amp; Future Scope</h2>

<h3 class="sub">9.1 Current Limitations</h3>
<table>
  <tr><th>Limitation</th><th>Reason</th><th>Production Fix</th></tr>
  <tr><td>GSTN API not called live</td><td>Requires MeitY GSTN API key (restricted)</td><td>Plug in GSTN sandbox credentials</td></tr>
  <tr><td>MCA21 data is mocked</td><td>MCA21 API requires corporate registration</td><td>MCA21 REST API integration</td></tr>
  <tr><td>EPFO/ESIC not implemented</td><td>Outside SIH demo scope</td><td>EPFO SHRAM portal API</td></tr>
  <tr><td>Bhashini in simulation mode</td><td>BHASHINI_TOKEN env variable not set</td><td>Set BHASHINI_TOKEN from ULCA dashboard</td></tr>
  <tr><td>Single officer role</td><td>No auth layer for hackathon</td><td>Add JWT auth + role-based access</td></tr>
  <tr><td>Single-bidder verification</td><td>Dropdown-based, not batch</td><td>Batch API + queue with Celery</td></tr>
</table>

<h3 class="sub">9.2 Future Scope</h3>
<ul>
  <li>Live integration: GSTN → PAN → MCA21 → EPFO → DigiLocker → Startup India → NSIC</li>
  <li>Multi-officer workflow with role-based approval gates</li>
  <li>Real-time Bhashini translation with ULCA production API token</li>
  <li>Batch tender evaluation — process 50+ bidders simultaneously</li>
  <li>LLM-based natural language recommendation generation (GPT-4/Gemini)</li>
  <li>Mobile-responsive officer app</li>
  <li>GeM portal direct integration for bidder self-submission</li>
  <li>DPDP-compliant PII redaction before audit storage</li>
</ul>

<div class="footer-line">
  <span>GeM AI Compliance Platform — SRS v1.0</span>
  <span>SIH 2026 | PS 26100 | CPCL / MoPNG</span>
  <span>September 2026 — Confidential</span>
</div>

</div>
</body>
</html>"""

OUT = "GEM_Compliance_SRS_v1.0.pdf"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(HTML, wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.pdf(
            path=OUT,
            format="A4",
            margin={"top": "1.5cm", "bottom": "1.5cm", "left": "1.8cm", "right": "1.8cm"},
            print_background=True,
        )
        await browser.close()
    print(f"Generated: {OUT}")

asyncio.run(main())
