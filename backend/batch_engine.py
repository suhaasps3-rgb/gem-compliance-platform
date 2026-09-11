"""
batch_engine.py — In-memory batch bidder processing engine.
Uses FastAPI BackgroundTasks (no Redis/Celery needed).
Processes ZIP archives containing bidder document folders.
Scores match the main Bidder Verification Dashboard / ComplianceScorecard.jsx exactly.
"""
import uuid
import zipfile
import io
import time
import json
import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from document_parsers import parse_epfo, parse_esic, parse_startup, parse_nsic, parse_work_order, parse_turnover_ca
from graph_engine import EvidenceGraphEngine
from experience_engine import validate_experience

# Global in-process state (matches existing global_audit_ledger pattern)
batch_registry: Dict[str, Dict] = {}

# Document type detection keywords (case-insensitive filename matching)
DOC_KEYWORDS = {
    "gst": ["gst", "gstin", "tax"],
    "udyam": ["udyam", "msme", "micro"],
    "epfo": ["epfo", "ecr", "provident", "pf"],
    "esic": ["esic", "esi"],
    "startup": ["startup", "dipp", "dpiit", "recognition"],
    "nsic": ["nsic"],
    "work_order": ["work_order", "workorder", "purchase_order", "po", "wo", "contract", "completion"],
    "turnover": ["turnover", "ca_cert", "balance_sheet", "audited", "financial"],
    "technical": ["technical", "catalog", "datasheet", "specification", "spec"],
    "debarment": ["debarment", "blacklisting", "non_debarment"],
    "bidder": ["technical_bid", "bid", "proposal"]
}


def _detect_doc_type(filename: str) -> str:
    lower = filename.lower()
    for doc_type, keywords in DOC_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return doc_type
    return "unknown"


def _find_matching_bidder(folder_name: str) -> Optional[Dict]:
    """Find matching bidder in database/mock_dataset.json by folder name."""
    fn = folder_name.lower().replace("_", "").replace("-", "").replace(" ", "")
    json_path = os.path.join(os.path.dirname(__file__), "..", "database", "mock_dataset.json")
    if not os.path.exists(json_path):
        json_path = "database/mock_dataset.json"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for b in data.get("bidders", []):
                bid_clean = b["id"].lower().replace("-", "").replace("_", "")
                name_clean = b["name"].lower().replace("-", "").replace("_", "").replace(" ", "")
                if fn in bid_clean or fn in name_clean or bid_clean in fn or any(token in fn for token in name_clean.split() if len(token) > 3):
                    return b
    except Exception:
        pass
    return None


def _compute_compliance_score(
    overall_status: str = "VERIFIED_COMPLIANT",
    contradictions: int = 0,
    gst_result: Optional[Dict] = None,
    udyam_result: Optional[Dict] = None,
    epfo_result: Optional[Dict] = None,
    esic_result: Optional[Dict] = None,
    startup_result: Optional[Dict] = None,
    experience_result: Optional[Dict] = None,
    technical_result: Optional[Dict] = None,
    visual_auth_result: Optional[Dict] = None
) -> tuple:
    """
    Compute a 0-100 compliance score and risk level.
    Uses the exact same deduction rules as ComplianceScorecard.jsx on the frontend.
    """
    score = 100

    # 1. Deduct based on overall backend status if viewing a known bidder
    if overall_status == 'NEEDS_REVIEW':
        score -= 15
    elif overall_status in ['REJECTED', 'NON_COMPLIANT']:
        score -= 50

    # 2. Deduct based on graph contradictions (-20 per contradiction)
    score -= (contradictions * 20)

    # 3. GST Verification deductions
    if gst_result:
        ver = gst_result.get("verification", {})
        if ver.get("composition_fail"):
            score -= 30
        elif not ver.get("gstin_found", True):
            score -= 15

    # 4. Udyam Verification deductions
    if udyam_result:
        ver = udyam_result.get("verification", {})
        if ver and not ver.get("is_micro", False):
            score -= 20

    # 5. EPFO Verification deductions
    if epfo_result:
        ver = epfo_result.get("verification", {})
        status = ver.get("contribution_status")
        if status == 'PENDING':
            score -= 10
        elif status == 'MISSING':
            score -= 15

    # 6. Experience requirement deductions
    if experience_result:
        if experience_result.get("result") == "FAIL":
            score -= 20
        elif experience_result.get("result") == "INSUFFICIENT_EVIDENCE":
            score -= 10

    # 7. Technical Matrix deductions
    if technical_result and technical_result.get("overall_result") == "FAIL":
        score -= 25

    # 8. Visual authenticity (missing signature/stamp)
    if visual_auth_result and not visual_auth_result.get("is_signed_and_stamped", True):
        score -= 50

    final_score = max(0, score)

    # Risk level (matches ComplianceScorecard.jsx EXACTLY)
    if final_score < 40:
        risk = "CRITICAL"
    elif final_score < 60:
        risk = "HIGH"
    elif final_score < 80:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return final_score, risk


def create_batch(zip_bytes: bytes) -> str:
    """Parse ZIP, identify bidder folders, initialize batch state."""
    batch_id = str(uuid.uuid4())[:8].upper()

    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    names = zf.namelist()

    # Identify bidder folders (top-level directories)
    bidder_folders = set()
    for name in names:
        parts = name.split("/")
        if len(parts) >= 2 and parts[0] and not parts[0].startswith("__"):
            bidder_folders.add(parts[0])

    if not bidder_folders:
        raise ValueError("No bidder folders found in ZIP. Expected: BidderName/document.pdf")

    bidders = {}
    for folder in sorted(bidder_folders):
        folder_files = [n for n in names if n.startswith(folder + "/") and n.endswith(".pdf")]
        doc_count = len(folder_files)
        bidders[folder] = {
            "name": folder.replace("_", " ").replace("-", " ").title(),
            "documents": [f.split("/", 1)[1] for f in folder_files],
            "doc_count": doc_count,
            "status": "QUEUED",
            "compliance_score": None,
            "risk_level": None,
            "contradictions": 0,
            "gst_result": None,
            "udyam_result": None,
            "epfo_result": None,
            "experience_result": None,
            "technical_result": None,
            "error": None
        }

    batch_registry[batch_id] = {
        "status": "QUEUED",
        "created_at": datetime.utcnow().isoformat(),
        "bidders": bidders,
        "summary": {
            "total": len(bidders),
            "processed": 0,
            "low_risk": 0,
            "medium_risk": 0,
            "high_risk": 0,
            "critical_risk": 0,
            "failed": 0
        }
    }
    return batch_id


def process_batch_background(batch_id: str, zip_bytes: bytes):
    """Background task: process each bidder's documents in the batch."""
    if batch_id not in batch_registry:
        return

    batch_registry[batch_id]["status"] = "PROCESSING"
    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    bidders = batch_registry[batch_id]["bidders"]

    for folder_name, bidder_entry in bidders.items():
        bidder_entry["status"] = "PROCESSING"
        try:
            time.sleep(0.6)

            work_orders_parsed = []
            gst_result = None
            udyam_result = None
            epfo_result = None
            esic_result = None
            startup_result = None
            visual_auth_result = None
            overall_status = "VERIFIED_COMPLIANT"
            contradictions = 0

            # 1. Match against known bidder in mock_dataset if available
            matched_bidder = _find_matching_bidder(folder_name)
            if matched_bidder:
                try:
                    engine = EvidenceGraphEngine(matched_bidder)
                    engine.build_graph()
                    res = engine.resolve_contradictions()
                    overall_status = res.get("status", "VERIFIED_COMPLIANT")
                    contradictions = len(res.get("contradictions", []))
                except Exception:
                    pass

            tech_result = None

            # 2. Process each document in the folder
            for doc_name in bidder_entry.get("documents", []):
                full_path = f"{folder_name}/{doc_name}"
                try:
                    doc_bytes = zf.read(full_path)
                except Exception:
                    continue

                doc_type = _detect_doc_type(doc_name)

                try:
                    if doc_type == "gst":
                        import pymupdf
                        doc = pymupdf.open(stream=doc_bytes, filetype="pdf")
                        text = " ".join(p.get_text() for p in doc)
                        m = re.search(r'Type of Registration[:\s]+(\w+)', text, re.IGNORECASE)
                        reg_type = m.group(1).title() if m else "Regular"
                        is_composition = "composition" in reg_type.lower()
                        gst_result = {
                            "document_type": "GST_CERTIFICATE",
                            "verification": {
                                "registration_type": reg_type,
                                "is_regular_taxpayer": not is_composition,
                                "composition_fail": is_composition,
                                "gstin_found": True
                            }
                        }
                    elif doc_type == "udyam":
                        from document_parsers import _extract_text
                        text2 = _extract_text(doc_bytes)
                        m2 = re.search(r'(?:Enterprise Classification|Type of Enterprise|Enterprise Type)[:\s]+(MICRO|SMALL|MEDIUM)', text2, re.IGNORECASE)
                        classification = m2.group(1).upper() if m2 else "MICRO"
                        udyam_result = {
                            "document_type": "UDYAM_CERTIFICATE",
                            "verification": {
                                "enterprise_classification": classification,
                                "is_micro": classification == "MICRO",
                                "is_msme": classification in ["MICRO", "SMALL", "MEDIUM"]
                            }
                        }
                    elif doc_type == "epfo":
                        epfo_result = parse_epfo(doc_bytes)
                    elif doc_type == "esic":
                        esic_result = parse_esic(doc_bytes)
                    elif doc_type == "startup":
                        startup_result = parse_startup(doc_bytes)
                    elif doc_type == "work_order":
                        wo = parse_work_order(doc_bytes)
                        work_orders_parsed.append(wo)
                        # Check signature on work order
                        try:
                            from visual_authenticity import verify_signature_and_stamp
                            auth = verify_signature_and_stamp(doc_bytes)
                            if not auth.get("is_signed_and_stamped"):
                                visual_auth_result = auth
                        except Exception:
                            pass
                    elif doc_type == "technical":
                        try:
                            from technical_eval import extract_specs_from_pdf, evaluate_technical_specs
                            from main import STANDARD_TENDER_SPECS
                            v_specs = extract_specs_from_pdf(doc_bytes)
                            if v_specs:
                                tech_result = evaluate_technical_specs(STANDARD_TENDER_SPECS, v_specs)
                        except Exception:
                            pass
                except Exception:
                    pass

            # 3. Experience & Technical validation
            exp_result = None
            if work_orders_parsed:
                exp_result = validate_experience(work_orders_parsed, requirement_cr=5.0)
            elif matched_bidder:
                raw_wos = matched_bidder.get("work_orders", [])
                if raw_wos:
                    formatted_wos = []
                    for wo in raw_wos:
                        formatted_wos.append({
                            "extracted": {
                                "wo_number": wo.get("wo_number"),
                                "client": wo.get("client"),
                                "order_value_cr": wo.get("value_cr"),
                                "order_date": wo.get("order_date"),
                                "execution_status": "COMPLETED"
                            },
                            "verification": {
                                "value_extracted": True,
                                "extraction_confidence": wo.get("confidence", 0.9)
                            }
                        })
                    exp_result = validate_experience(formatted_wos, requirement_cr=5.0, eligible_years=5)

            if not tech_result and matched_bidder:
                try:
                    from main import STANDARD_TENDER_SPECS
                    from technical_eval import evaluate_technical_specs
                    raw_specs = matched_bidder.get("technical_specs", {})
                    if raw_specs:
                        vendor_specs_list = [{"parameter": k, "vendor_value": v} for k, v in raw_specs.items()]
                        tech_result = evaluate_technical_specs(STANDARD_TENDER_SPECS, vendor_specs_list)
                except Exception:
                    pass

            # 4. Calculate Unified Compliance Score (matching Dashboard 1:1)
            score, risk = _compute_compliance_score(
                overall_status=overall_status,
                contradictions=contradictions,
                gst_result=gst_result,
                udyam_result=udyam_result,
                epfo_result=epfo_result,
                esic_result=esic_result,
                startup_result=startup_result,
                experience_result=exp_result,
                technical_result=tech_result,
                visual_auth_result=visual_auth_result
            )

            bidder_entry.update({
                "status": "COMPLETED",
                "compliance_score": score,
                "risk_level": risk,
                "contradictions": contradictions,
                "gst_result": gst_result,
                "udyam_result": udyam_result,
                "epfo_result": epfo_result,
                "experience_result": exp_result,
                "technical_result": tech_result
            })

        except Exception as e:
            bidder_entry.update({
                "status": "FAILED",
                "error": str(e),
                "compliance_score": 0,
                "risk_level": "CRITICAL"
            })

    # Update summary
    summary = batch_registry[batch_id]["summary"]
    for b in bidders.values():
        if b["status"] in ["COMPLETED", "PARTIAL"]:
            summary["processed"] += 1
            risk = b.get("risk_level", "CRITICAL")
            if risk == "LOW": summary["low_risk"] += 1
            elif risk == "MEDIUM": summary["medium_risk"] += 1
            elif risk == "HIGH": summary["high_risk"] += 1
            else: summary["critical_risk"] += 1
        elif b["status"] == "FAILED":
            summary["failed"] += 1

    batch_registry[batch_id]["status"] = "COMPLETED"


def get_batch_state(batch_id: str) -> Optional[Dict]:
    return batch_registry.get(batch_id)
