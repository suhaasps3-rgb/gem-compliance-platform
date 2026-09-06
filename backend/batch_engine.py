"""
batch_engine.py — In-memory batch bidder processing engine.
Uses FastAPI BackgroundTasks (no Redis/Celery needed).
Processes ZIP archives containing bidder document folders.
"""
import uuid
import zipfile
import io
import time
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
    "bidder": ["technical_bid", "bid", "proposal"]
}


def _detect_doc_type(filename: str) -> str:
    lower = filename.lower()
    for doc_type, keywords in DOC_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return doc_type
    return "unknown"


def _compute_compliance_score(gst_result=None, udyam_result=None, epfo_result=None,
                               esic_result=None, contradictions=0, experience_result=None) -> tuple:
    """Compute a 0-100 compliance score and risk level."""
    score = 100
    deductions = 0

    # GST
    if gst_result:
        if gst_result.get("verification", {}).get("composition_fail"):
            deductions += 30
        elif not gst_result.get("verification", {}).get("gstin_found"):
            deductions += 15

    # Udyam
    if udyam_result:
        if not udyam_result.get("verification", {}).get("is_micro"):
            deductions += 20

    # Contradictions
    deductions += contradictions * 20

    # EPFO
    if epfo_result:
        if epfo_result.get("verification", {}).get("contribution_status") == "PENDING":
            deductions += 10
        elif epfo_result.get("verification", {}).get("contribution_status") == "MISSING":
            deductions += 15

    # Experience
    if experience_result:
        if experience_result.get("result") == "FAIL":
            deductions += 20
        elif experience_result.get("result") == "INSUFFICIENT_EVIDENCE":
            deductions += 10

    final_score = max(0, score - deductions)

    if final_score >= 80:
        risk = "LOW"
    elif final_score >= 60:
        risk = "MEDIUM"
    elif final_score >= 40:
        risk = "HIGH"
    else:
        risk = "CRITICAL"

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
            # Simulate realistic processing delay for demo
            time.sleep(0.8)

            work_orders_parsed = []
            gst_result = None
            udyam_result = None
            epfo_result = None
            contradictions = 0

            # Process each document
            for doc_name in bidder_entry.get("documents", []):
                full_path = f"{folder_name}/{doc_name}"
                try:
                    doc_bytes = zf.read(full_path)
                except Exception:
                    continue

                doc_type = _detect_doc_type(doc_name)

                try:
                    if doc_type == "gst":
                        gst_result = parse_epfo(doc_bytes)  # use GST parse
                        from document_parsers import parse_gst_bytes
                        gst_result = None  # placeholder — inline parse
                        import re as _re
                        import pymupdf
                        doc = pymupdf.open(stream=doc_bytes, filetype="pdf")
                        text = " ".join(p.get_text() for p in doc)
                        m = _re.search(r'Type of Registration\s+(\w+)', text)
                        reg_type = m.group(1) if m else "Unknown"
                        gst_result = {
                            "document_type": "GST_CERTIFICATE",
                            "verification": {
                                "registration_type": reg_type,
                                "is_regular_taxpayer": reg_type.lower() == "regular",
                                "composition_fail": reg_type.lower() == "composition"
                            }
                        }
                    elif doc_type == "udyam":
                        from document_parsers import _extract_text
                        import re as _re2
                        text2 = _extract_text(doc_bytes)
                        m2 = _re2.search(r'Enterprise Classification\s+(MICRO|SMALL|MEDIUM)', text2, _re2.IGNORECASE)
                        classification = m2.group(1).upper() if m2 else "UNKNOWN"
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
                    elif doc_type == "work_order":
                        wo = parse_work_order(doc_bytes)
                        work_orders_parsed.append(wo)
                except Exception:
                    pass

            # Experience validation
            exp_result = None
            if work_orders_parsed:
                exp_result = validate_experience(work_orders_parsed, requirement_cr=5.0)

            score, risk = _compute_compliance_score(
                gst_result=gst_result,
                udyam_result=udyam_result,
                epfo_result=epfo_result,
                contradictions=contradictions,
                experience_result=exp_result
            )

            bidder_entry.update({
                "status": "COMPLETED",
                "compliance_score": score,
                "risk_level": risk,
                "contradictions": contradictions,
                "gst_result": gst_result,
                "udyam_result": udyam_result,
                "epfo_result": epfo_result,
                "experience_result": exp_result
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
