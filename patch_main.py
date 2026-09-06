import os

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance'
f = os.path.join(ROOT, 'backend', 'main.py')

with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

new_endpoints = """
# ──────────────────────────────────────────────────────
# NEW ENDPOINTS — Document Parsers (EPFO, ESIC, Startup, NSIC, WO, Turnover)
# ──────────────────────────────────────────────────────
from document_parsers import parse_epfo, parse_esic, parse_startup, parse_nsic, parse_work_order, parse_turnover_ca
from experience_engine import validate_experience
from technical_eval import evaluate_technical_specs, extract_specs_from_pdf
from batch_engine import batch_registry, create_batch, get_batch_state
import zipfile
import io

@app.post("/api/v1/bidders/parse-epfo")
async def parse_epfo_doc(epfo_pdf: UploadFile = File(...)):
    file_bytes = await epfo_pdf.read()
    return parse_epfo(file_bytes)

@app.post("/api/v1/bidders/parse-esic")
async def parse_esic_doc(esic_pdf: UploadFile = File(...)):
    file_bytes = await esic_pdf.read()
    return parse_esic(file_bytes)

@app.post("/api/v1/bidders/parse-startup")
async def parse_startup_doc(startup_pdf: UploadFile = File(...)):
    file_bytes = await startup_pdf.read()
    return parse_startup(file_bytes)

@app.post("/api/v1/bidders/parse-nsic")
async def parse_nsic_doc(nsic_pdf: UploadFile = File(...)):
    file_bytes = await nsic_pdf.read()
    return parse_nsic(file_bytes)

@app.post("/api/v1/bidders/parse-work-order")
async def parse_work_order_doc(wo_pdf: UploadFile = File(...)):
    file_bytes = await wo_pdf.read()
    return parse_work_order(file_bytes)

@app.post("/api/v1/bidders/parse-turnover")
async def parse_turnover_doc(turnover_pdf: UploadFile = File(...)):
    file_bytes = await turnover_pdf.read()
    return parse_turnover_ca(file_bytes)

@app.post("/api/v1/bidders/validate-experience")
async def validate_bidder_experience(
    requirement_cr: float = Form(...),
    eligible_years: int = Form(default=5),
    wo_results: str = Form(...)  # JSON string of work order result list
):
    import json
    try:
        work_orders = json.loads(wo_results)
    except Exception:
        raise HTTPException(status_code=400, detail="wo_results must be a JSON array of work order parse results")
    return validate_experience(work_orders, requirement_cr, eligible_years)

@app.post("/api/v1/technical/evaluate")
async def technical_evaluate(
    tender_specs: str = Form(...),   # JSON list of {parameter, operator, required_value, unit}
    vendor_pdf: Optional[UploadFile] = File(None),
    vendor_specs: Optional[str] = Form(None)  # JSON list of {parameter, vendor_value}
):
    import json
    try:
        t_specs = json.loads(tender_specs)
    except Exception:
        raise HTTPException(status_code=400, detail="tender_specs must be valid JSON")

    if vendor_pdf:
        file_bytes = await vendor_pdf.read()
        v_specs = extract_specs_from_pdf(file_bytes)
        if not v_specs and vendor_specs:
            v_specs = json.loads(vendor_specs)
    elif vendor_specs:
        v_specs = json.loads(vendor_specs)
    else:
        raise HTTPException(status_code=400, detail="Provide either vendor_pdf or vendor_specs")

    return evaluate_technical_specs(t_specs, v_specs)

@app.get("/api/v1/cartel/metadata-fingerprint")
async def cartel_metadata_fingerprint():
    \"\"\"Analyze PDF metadata clusters from mock dataset.\"\"\"
    mock_data = load_mock_data()
    bidders = mock_data.get("bidders", [])
    engine = CollusionEngine(bidders)
    clusters = engine.get_metadata_clusters(bidders)
    return {
        "status": "ANALYSIS_COMPLETE",
        "clusters": clusters,
        "total_suspicious_clusters": len(clusters),
        "disclaimer": "Metadata similarity is a suspicious indicator only. Not definitive proof of collusion."
    }

@app.get("/api/v1/cartel/network-risk")
async def cartel_network_risk():
    \"\"\"Analyze IP/network overlap from mock submission metadata.\"\"\"
    mock_data = load_mock_data()
    bidders = mock_data.get("bidders", [])
    engine = CollusionEngine(bidders)
    clusters = engine.get_ip_clusters(bidders)
    return {
        "status": "ANALYSIS_COMPLETE",
        "ip_clusters": clusters,
        "total_clusters": len(clusters),
        "disclaimer": "SIMULATED DEMONSTRATION DATA. IP overlap does not constitute proof of collusion."
    }

# ──────────────────────────────────────────────────────
# BATCH PROCESSING
# ──────────────────────────────────────────────────────
from fastapi import BackgroundTasks
from batch_engine import process_batch_background

@app.post("/api/v1/batch/upload")
async def batch_upload(
    background_tasks: BackgroundTasks,
    batch_zip: UploadFile = File(...)
):
    \"\"\"Accept a ZIP of bidder folders. Identify bidders. Start background processing.\"\"\"
    zip_bytes = await batch_zip.read()
    try:
        batch_id = create_batch(zip_bytes)
        background_tasks.add_task(process_batch_background, batch_id, zip_bytes)
        state = get_batch_state(batch_id)
        return {
            "batch_id": batch_id,
            "status": "QUEUED",
            "bidders_identified": list(state["bidders"].keys()),
            "bidder_count": len(state["bidders"])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process ZIP: {str(e)}")

@app.get("/api/v1/batch/{batch_id}")
async def get_batch(batch_id: str):
    state = get_batch_state(batch_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return state

@app.get("/api/v1/batch/{batch_id}/status")
async def get_batch_status(batch_id: str):
    state = get_batch_state(batch_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    bidders = state.get("bidders", {})
    processed = sum(1 for b in bidders.values() if b["status"] in ["COMPLETED", "PARTIAL", "FAILED"])
    total = len(bidders)
    return {
        "batch_id": batch_id,
        "status": state["status"],
        "total": total,
        "processed": processed,
        "progress_pct": round(processed / total * 100, 1) if total > 0 else 0,
        "summary": state.get("summary", {})
    }
"""

if "parse_epfo" not in content:
    content = content.replace('if __name__ == "__main__":', new_endpoints + '\nif __name__ == "__main__":')

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

    print('main.py updated.')
else:
    print('main.py already has new endpoints.')
