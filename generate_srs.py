import asyncio
from playwright.async_api import async_playwright

srs_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; margin: 40px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 40px; }
        h2 { color: #2980b9; margin-top: 30px; }
        h3 { color: #34495e; }
        p { text-align: justify; }
        .cover { text-align: center; margin-top: 150px; margin-bottom: 200px; }
        .cover h1 { border: none; font-size: 3em; color: #2c3e50; }
        .cover h2 { color: #7f8c8d; font-weight: 300; }
        .cover h3 { margin-top: 50px; color: #95a5a6; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; margin-bottom: 20px; }
        th, td { border: 1px solid #bdc3c7; padding: 12px; text-align: left; }
        th { background-color: #ecf0f1; }
        .page-break { page-break-after: always; }
        ul { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="cover">
        <h1>Software Requirements Specification (SRS)</h1>
        <h2>GeM Compliance - AI Verification Platform</h2>
        <h3>Prepared for: SIH 2026 (Problem Statement 26100 - CPCL)</h3>
        <h3>Version 1.0</h3>
    </div>
    
    <div class="page-break"></div>

    <h1>1. Introduction</h1>
    <h2>1.1 Purpose</h2>
    <p>The purpose of this document is to detail the software requirements for the GeM Compliance AI Verification Platform. This system automates the tedious, error-prone manual verification of bidder documents, dynamically detects fraud, and flags cartelization behavior for the Government e-Marketplace (GeM).</p>
    
    <h2>1.2 Scope</h2>
    <p>The platform replaces manual verification with an automated, deterministic pipeline. It processes PDF proofs (Turnover, MSME, Tax, Experience), cross-references them against live/mocked APIs using a Graph Engine, evaluates financial thresholds, and translates regional language documents using MeitY Bhashini AI.</p>
    
    <h1>2. System Architecture</h1>
    <h2>2.1 End-to-End Procurement Workflow</h2>
    <div style="background: #f1f5f9; padding: 15px; border-left: 4px solid #3b82f6; margin-bottom: 20px; font-size: 13px;">
        1. Document Upload → 2. Document Classification → 3. Text Extraction (PyMuPDF / OCR) → 4. Data Extraction → 5. Document Validation → 6. Missing Document Detection → 7. OEM Authorization Verification → 8. DigiLocker Verification → 9. Blacklisting / Debarment Check → 10. Compliance Matrix / Hard Filters → 11. Compliance Score → 12. AI Recommendation Engine → 13. Procurement Officer Review → 14. Final Procurement Officer Decision → 15. Final Compliance Report
    </div>
    
    <h2>2.2 Tech Stack</h2>
    <table>
        <tr><th>Layer</th><th>Technology</th><th>Purpose</th></tr>
        <tr><td>Frontend</td><td>React 18, Vite, Tailwind CSS, Zustand, ReactFlow</td><td>Interactive dashboards, real-time batch monitoring, and evidence provenance graphs.</td></tr>
        <tr><td>Backend</td><td>Python, FastAPI, BackgroundTasks</td><td>High-performance API handling, concurrent batch processing, and rule evaluation.</td></tr>
        <tr><td>Graph Engine</td><td>NetworkX</td><td>Detecting multi-node contradictions and cartelization patterns across bidders.</td></tr>
        <tr><td>Data Parsing</td><td>PyMuPDF, Regex (Zero-LLM)</td><td>Deterministic, sub-5ms extraction of structured data from complex PDFs without PII exposure.</td></tr>
    </table>

    <div class="page-break"></div>

    <h1>3. Core Features & Requirements</h1>
    <h2>3.1 Intelligent Document Parsing (PyMuPDF / OCR)</h2>
    <p>The system shall determine extractability and use <strong>PyMuPDF</strong> for digitally generated PDFs, and <strong>Tesseract/Bhashini OCR</strong> for scanned documents. Data is then extracted via deterministic RegEx/AI capture groups:</p>
    <ul>
        <li><b>Financial:</b> CA Turnover Certificates, Work Orders / Purchase Orders.</li>
        <li><b>Statutory:</b> GST REG-06, Udyam Registration.</li>
        <li><b>Labor & HR:</b> EPFO ECR Statements, ESIC Challans.</li>
        <li><b>Exemptions:</b> Startup India Certificates (DIPP), NSIC Certificates.</li>
    </ul>

    <h3>3.1.1 Visual Authenticity Verification Module</h3>
    <p>The system shall programmatically analyze the lower bounds of all statutory declarations for the presence of embedded graphic elements or color-profile anomalies (e.g., blue/violet ink pixel density). Documents lacking a detectable physical stamp or authorized digital signature object shall be flagged for manual Officer Review.</p>

    <h2>3.2 Graph-Based Contradiction Engine</h2>
    <p>The system shall construct an Evidence Provenance Graph. If a bidder claims "Micro" status (Turnover &lt; 5Cr) via an uploaded Udyam certificate, but the backend MCA21 API node reports a turnover of 14.5Cr, the Graph Engine shall generate a deterministic red conflict edge and deduct compliance points.</p>

    <h2>3.3 Multi-Document Experience Aggregator</h2>
    <p>The system shall extract financial values from an unbounded number of Work Orders. The Experience Engine will mathematically aggregate valid work orders (e.g., 2.1 Cr + 1.75 Cr) and validate them against tender-specific limits (e.g., Min 5.0 Cr) to issue a definitive PASS/FAIL metric.</p>

    <h2>3.4 GST Return Filing & Validation Module</h2>
    <p>The platform extends beyond static GST REG-06 certificate parsing by integrating with a Mock GSTN API to verify live compliance:</p>
    <ul>
        <li><b>GSTIN Verification:</b> Registration status, legal name matching, and cancellation status.</li>
        <li><b>Return Filing Status:</b> Validates whether the bidder has filed returns for the relevant filing period, flagging <i>Pending ⚠️</i> statuses directly on the dashboard.</li>
        <li><b>Mismatch Detection:</b> Automatically cross-checks the submitted document data against the live portal data.</li>
    </ul>

    <h2>3.5 PAN & Income Tax (ITR) Verification</h2>
    <p>The Graph Engine executes a multi-way cross-check to prevent identity spoofing and tax evasion:</p>
    <ul>
        <li><b>Entity Cross-Check:</b> Bidder Name ↔️ PAN ↔️ GST Registered Name ↔️ MCA21 Company Name. Any discrepancy (e.g., mismatch in corporate structure) raises a <i>CONFLICT ⚠️</i> flag.</li>
        <li><b>Income Tax Compliance:</b> Validates the relevant financial year ITR filing status via mock API, mapping the submitted proof against portal verification to ensure tax compliance.</li>
    </ul>

    <h2>3.6 Make in India (MII) / Local Content Compliance</h2>
    <p>Directly addressing CPCL requirement #5, the system programmatically evaluates Make in India (Public Procurement) declarations:</p>
    <ul>
        <li><b>Data Extraction:</b> Extracts Local Content %, Supplier Classification (e.g., Class-I), Country of Origin, and supporting declarations from the bidder's submissions.</li>
        <li><b>Threshold Evaluation:</b> Automatically compares the extracted Local Content % against the Tender's minimum requirement (e.g., Tender Minimum = 50%, Bidder = 62% → <i>PASS ✅</i>).</li>
        <li><b>Enforcement:</b> Missing declarations or percentages below the threshold are flagged for immediate manual review or automatic failure.</li>
    </ul>

    <h2>3.7 Anti-Cartelization Network Scanner</h2>
    <p>The backend shall run Jaccard Similarity algorithms across the entire submitted batch of bidders to detect collusion rings, such as multiple bidders sharing the same MCA21 directors, identical technical catalog specs, or identical sub-contractor networks.</p>

    <h2>3.8 Batch Processing Pipeline</h2>
    <p>The system shall support bulk ZIP uploads. Utilizing FastAPI BackgroundTasks, the pipeline will concurrently unpack directories, detect document types heuristically, invoke modular parsers, and stream real-time pipeline status (0-100%) to the frontend Batch Dashboard.</p>

    <h2>3.9 Bhashini Regional Translation</h2>
    <p>The system shall integrate with MeitY Bhashini AI to process regional language tender documents (e.g., Hindi, Tamil), translating them seamlessly into English for unified English-based rule compilation.</p>

    <h2>3.10 OEM Authorization Verification</h2>
    <p>The system shall dynamically verify OEM authorization documents, extracting OEM names, dealer identities, and validity periods. The compliance matrix tracks statuses explicitly as <strong>Verified</strong>, <strong>Invalid</strong>, <strong>Expired</strong>, or <strong>Missing</strong>.</p>

    <h2>3.11 DigiLocker Verification</h2>
    <p>A native integration (or mocked equivalent for demo purposes) checks whether a submitted document matches official DigiLocker records, returning statuses of <strong>Verified</strong>, <strong>Not Verified</strong>, or <strong>Unavailable</strong> to ensure document provenance.</p>

    <h2>3.12 Blacklisting & Debarment Check</h2>
    <p>A dedicated module queries vigilance and compliance databases to verify if a vendor is debarred from government procurement. The system flags vendors as <strong>CLEAR</strong>, <strong>BLACKLISTED</strong>, <strong>DEBARRED</strong>, or <strong>UNABLE TO VERIFY</strong>, treating blacklisting as a critical compliance failure.</p>

    <h2>3.13 Missing-Document Detection</h2>
    <p>The Graph Engine dynamically compares the mandatory required documents defined in the tender configuration against the actual documents uploaded by the bidder. Missing documents are explicitly listed on the dashboard and immediately negatively impact the compliance recommendation.</p>

    <h2>3.14 AI Recommendation Engine (Advisory)</h2>
    <p>The platform aggregates the compliance score, missing documents, contradictions, OEM authorizations, and financial validation into an AI Recommendation Engine. It produces an explicit, advisory decision: <strong>RECOMMENDED</strong>, <strong>NOT RECOMMENDED</strong>, or <strong>REQUIRES CLARIFICATION</strong>, accompanied by human-readable reasoning and specific red flags.</p>

    <h2>3.15 Procurement Officer Final Decision (Authoritative)</h2>
    <p>To ensure strict accountability, the workflow terminates with a Procurement Officer decision block. The PO reviews the AI's advisory recommendation, the evidence provenance graph, and all extracted flags, then issues the final, authoritative decision (<strong>Approve</strong>, <strong>Reject</strong>, or <strong>Request Clarification</strong>), which permanently supersedes the AI output.</p>

    
    <h1>4. Non-Functional Requirements</h1>
    <h2>4.1 Security & Data Privacy</h2>
    <p>The system operates under a Zero-LLM policy for data extraction to ensure Data Protection (DPDP Act) compliance. No Personally Identifiable Information (PII) is sent to external AI servers. All parsing is deterministic and local.</p>
    
    <h2>4.2 Auditability</h2>
    <p>All automated decisions (Verification passes, contradiction flags, risk level assignments) shall be cryptographically hashed (SHA-256) to create an immutable audit ledger, ensuring decisions can be defended during post-tender vigilance inquiries.</p>

</body>
</html>
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(srs_html)
        await page.pdf(path="GeM_Compliance_SRS.pdf", format="A4", margin={"top": "1in", "bottom": "1in", "left": "1in", "right": "1in"})
        await browser.close()
        print("Generated GeM_Compliance_SRS.pdf")

if __name__ == "__main__":
    asyncio.run(main())
