from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import os
from graph_engine import EvidenceGraphEngine
from collusion_engine import CollusionEngine
from rule_compiler import TenderRuleCompiler
from audit_engine import AuditEngine

global_audit_ledger = AuditEngine()

app = FastAPI(
    title="GeM Compliance Engine API",
    description="Evidence Provenance Graph Platform for Hackathon",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon/development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load mock dataset
MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "mock_dataset.json")
def load_mock_data():
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------------------
# Pydantic Models for Mock/API Responses
# -----------------------------------------
class ExtractedRule(BaseModel):
    clause: str
    description: str
    mapped_regulatory_id: str

class CompileRulesResponse(BaseModel):
    status: str
    extracted_rules: List[ExtractedRule]

class DeterministicAnchors(BaseModel):
    PAN: str
    PAN_confidence: str
    corroboration: str

class IngestDocumentResponse(BaseModel):
    document_id: str
    status: str
    deterministic_anchors: DeterministicAnchors
    extracted_claims: dict

class VerifyBidderResponse(BaseModel):
    verification_job_id: str
    status: str
    graph_persisted: bool
    contradictions_found: int

class DashboardResponse(BaseModel):
    overall_status: str
    hard_filters: dict
    scores: dict
    graph_data: dict
    active_contradictions: List[dict]

class OfficerDecisionRequest(BaseModel):
    bidder_id: str
    contradiction_id: str
    action: str
    rule_citation_id: str
    escalation_flag_id: str
    justification: str

class OfficerDecisionResponse(BaseModel):
    status: str
    audit_hash: str
    generated_notice_url: str
    generated_notice_text: str

class InvestigativeLead(BaseModel):
    lead_type: str
    bidders_involved: List[str]
    evidence: List[str]
    disclaimer: str

class CollusionSignalsResponse(BaseModel):
    status: str
    investigative_leads: List[InvestigativeLead]

# -----------------------------------------
# Core Endpoints
# -----------------------------------------

@app.post("/api/v1/tenders/{tender_id}/compile-rules", response_model=CompileRulesResponse)
async def compile_rules(tender_id: str, tender_pdf: UploadFile = File(...)):
    """
    Extracts clauses from an uploaded Tender PDF using an LLM and maps them to structured requirements.
    """
    compiler = TenderRuleCompiler()
    
    # Read file bytes (simulated for LLM)
    file_bytes = await tender_pdf.read()
    
    extracted_data = compiler.extract_rules_from_pdf(file_bytes, tender_pdf.filename)
    
    rules = [ExtractedRule(**rule) for rule in extracted_data]
    
    return CompileRulesResponse(
        status="COMPILED",
        extracted_rules=rules
    )

@app.post("/api/v1/ingest/document", response_model=IngestDocumentResponse)
async def ingest_document(
    bidder_id: str = Form(...),
    tender_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Accepts bidder PDFs, stores in S3, masks PII, and runs the OCR/Extraction pipeline.
    """
    return IngestDocumentResponse(
        document_id=str(uuid.uuid4()),
        status="EXTRACTED",
        deterministic_anchors=DeterministicAnchors(
            PAN="ABCDE1234F",
            PAN_confidence="HIGH",
            corroboration="GSTIN_MATCH"
        ),
        extracted_claims={
            "financial_turnover_cr": 8.5,
            "is_msme": True
        }
    )

@app.post("/api/v1/verify/bidder/{bidder_id}/tender/{tender_id}", response_model=VerifyBidderResponse)
async def verify_bidder(bidder_id: str, tender_id: str):
    """
    Spawns simulated API calls based on the PAN anchor. Builds NetworkX graph in-memory.
    """
    mock_data = load_mock_data()
    bidder_data = next((b for b in mock_data.get("bidders", []) if b["id"] == bidder_id), None)
    
    if not bidder_data:
        raise HTTPException(status_code=404, detail="Bidder not found in mock data")

    engine = EvidenceGraphEngine(bidder_data)
    engine.build_graph()
    results = engine.resolve_contradictions()
    
    return VerifyBidderResponse(
        verification_job_id=str(uuid.uuid4()),
        status=results["status"],
        graph_persisted=True,
        contradictions_found=len(results["contradictions"])
    )

@app.get("/api/v1/dashboard/bidder/{bidder_id}", response_model=DashboardResponse)
async def get_dashboard(bidder_id: str):
    """
    Feeds the React UI the 4-state result model, risk scores, and the graph data.
    """
    mock_data = load_mock_data()
    bidder_data = next((b for b in mock_data.get("bidders", []) if b["id"] == bidder_id), None)
    if not bidder_data:
        raise HTTPException(status_code=404, detail="Bidder not found")

    engine = EvidenceGraphEngine(bidder_data)
    engine.build_graph()
    results = engine.resolve_contradictions()
    
    return DashboardResponse(
        overall_status=results["status"],
        hard_filters={
            "pan_active": "PASS",
            "gst_active": "PASS",
            "not_debarred": "PASS"
        },
        scores={
            "evidence_confidence": 0.85,
            "probabilistic_risk": 65
        },
        graph_data=engine.serialize_graph(),
        active_contradictions=results["contradictions"]
    )

@app.get("/api/v1/tenders/{tender_id}/collusion-signals", response_model=CollusionSignalsResponse)
async def get_collusion_signals(tender_id: str):
    """
    Cross-bidder comparison mapping identical directors (MCA mock), shared IPs, etc.
    """
    mock_data = load_mock_data()
    bidders = mock_data.get("bidders", [])
    
    engine = CollusionEngine(bidders)
    results = engine.analyze_collusion(tender_id)
    
    return CollusionSignalsResponse(
        status=results["status"],
        investigative_leads=[InvestigativeLead(**lead) for lead in results["investigative_leads"]]
    )

@app.post("/api/v1/officer/decision", response_model=OfficerDecisionResponse)
async def officer_decision(request: OfficerDecisionRequest):
    """
    Records the statutory decision, drafts the show-cause notice, and cryptographically commits the action.
    """
    # 1. Generate Statutory Notice Text
    notice_text = (
        f"SHOW-CAUSE NOTICE\n\n"
        f"To: Bidder {request.bidder_id}\n\n"
        f"Under GFR 2017 Rule 175 (Code of Integrity), any omission or misrepresentation that may mislead "
        f"or attempt to mislead so that financial or other benefit may be obtained is strictly prohibited.\n\n"
        f"Basis of Notice: {request.justification}\n\n"
        f"Failure to respond within 72 hours may result in escalation to Debarment under DoE OM 08.05.2026 (amending GFR Rule 151).\n\n"
        f"Issued by: GeM Compliance Automated Review\n"
    )

    # 2. Commit to SHA-256 Ledger
    payload = {
        "bidder_id": request.bidder_id,
        "contradiction_id": request.contradiction_id,
        "action": request.action,
        "justification": request.justification,
        "notice_text": notice_text
    }
    audit_hash = global_audit_ledger.commit_audit_event("OFFICER_DECISION", payload)

    return OfficerDecisionResponse(
        status="SUCCESS",
        audit_hash=audit_hash,
        generated_notice_url=f"s3://bucket/notices/{uuid.uuid4()}.pdf",
        generated_notice_text=notice_text
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
