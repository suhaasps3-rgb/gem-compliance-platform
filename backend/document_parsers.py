"""
document_parsers.py — Modular PDF document parsers for GeM Compliance Platform.
Follows same pattern as parse-gst and parse-udyam endpoints in main.py.
All parsers accept raw PDF bytes and return structured extraction + verification dicts.
"""
import re
import pymupdf  # fitz
from datetime import datetime, date
from typing import Optional


def _extract_text(pdf_bytes: bytes) -> str:
    """Extract full text from PDF bytes using PyMuPDF."""
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        return " ".join(page.get_text() for page in doc)
    except Exception as e:
        return ""


def parse_epfo(pdf_bytes: bytes) -> dict:
    """Parse EPFO ECR/statement PDF. Extracts employer details and contribution status."""
    text = _extract_text(pdf_bytes)
    result = {
        "document_type": "EPFO_STATEMENT",
        "extracted": {},
        "verification": {},
        "source": "PDF_OCR"
    }

    # Employer name
    m = re.search(r'(?:Employer Name|Establishment Name)[:\s]+([A-Za-z][A-Za-z\s&\.]+?)(?=\n|\d|Employer Code)', text, re.IGNORECASE)
    if m:
        result["extracted"]["employer_name"] = m.group(1).strip()

    # Employer/Establishment code
    m = re.search(r'(?:Employer Code|Establishment Code|Est\.? No\.?)[:\s]*([A-Z]{2}[A-Z0-9]{4,20})', text, re.IGNORECASE)
    if m:
        result["extracted"]["employer_code"] = m.group(1).strip()

    # Employee count
    m = re.search(r'(?:No\.? of Employees|Employee Count|Total Employees)[:\s]*(\d+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["employee_count"] = int(m.group(1))

    # Contribution period
    m = re.search(r'(?:Wage Month|Period|Contribution Period)[:\s]+([A-Za-z]+[\s-]+\d{4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["contribution_period"] = m.group(1).strip()

    # Employee contribution
    m = re.search(r'(?:Employee Contribution|EE Share)[:\s]*(?:Rs\.?|₹)?[\s]*(\d[\d,\.]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["employee_contribution"] = m.group(1).replace(',', '')

    # Employer contribution
    m = re.search(r'(?:Employer Contribution|ER Share)[:\s]*(?:Rs\.?|₹)?[\s]*(\d[\d,\.]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["employer_contribution"] = m.group(1).replace(',', '')

    # Total amount
    m = re.search(r'(?:Total Contribution|Total Amount|Challan Amount)[:\s]*(?:Rs\.?|₹)?[\s]*(\d[\d,\.]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["total_contribution"] = m.group(1).replace(',', '')

    # Challan/transaction reference
    m = re.search(r'(?:Challan No|Transaction ID|Reference No)[:\s]*([A-Z0-9\-/]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["challan_reference"] = m.group(1).strip()

    # Payment status
    paid = bool(re.search(r'\b(PAID|Payment Successful|Challan Generated|Amount Credited)\b', text, re.IGNORECASE))
    pending = bool(re.search(r'\b(PENDING|UNPAID|Due|Overdue)\b', text, re.IGNORECASE))

    if paid:
        contribution_status = "PAID"
    elif pending:
        contribution_status = "PENDING"
    elif result["extracted"].get("total_contribution"):
        contribution_status = "UNVERIFIABLE"
    else:
        contribution_status = "MISSING"

    result["verification"] = {
        "employer_code_found": bool(result["extracted"].get("employer_code")),
        "contribution_status": contribution_status,
        "contribution_verified": paid,
        "employee_count_found": bool(result["extracted"].get("employee_count")),
        "source": "PDF_OCR",
        "note": "In production: verify via EPFO Unified Portal with employer code for live compliance status."
    }

    return result


def parse_esic(pdf_bytes: bytes) -> dict:
    """Parse ESIC challan/contribution statement PDF."""
    text = _extract_text(pdf_bytes)
    result = {
        "document_type": "ESIC_CONTRIBUTION_STATEMENT",
        "extracted": {},
        "verification": {},
        "source": "PDF_OCR"
    }

    # Employer name
    m = re.search(r'(?:Employer Name|Establishment Name)[:\s]+([A-Za-z][A-Za-z\s&\.]+?)(?=\n|\d|Code)', text, re.IGNORECASE)
    if m:
        result["extracted"]["employer_name"] = m.group(1).strip()

    # ESIC employer code
    m = re.search(r'(?:Employer Code|ESIC Code|Registration No)[:\s]*([\d]{17}|[A-Z0-9\-]{10,20})', text, re.IGNORECASE)
    if m:
        result["extracted"]["employer_code"] = m.group(1).strip()

    # Period
    m = re.search(r'(?:Contribution Period|Period)[:\s]+([A-Za-z]+[\s-]+\d{4}(?:[\s-]+to[\s-]+[A-Za-z]+[\s-]+\d{4})?)', text, re.IGNORECASE)
    if m:
        result["extracted"]["contribution_period"] = m.group(1).strip()

    # Employee count
    m = re.search(r'(?:No\.? of Employees|Insured Persons)[:\s]*(\d+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["employee_count"] = int(m.group(1))

    # Contribution amount
    m = re.search(r'(?:Total Contribution|Contribution Amount|Challan Amount)[:\s]*(?:Rs\.?|₹)?[\s]*(\d[\d,\.]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["contribution_amount"] = m.group(1).replace(',', '')

    # Challan reference
    m = re.search(r'(?:Challan No|Transaction Ref)[:\s]*([A-Z0-9/\-]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["challan_reference"] = m.group(1).strip()

    paid = bool(re.search(r'\b(PAID|Payment Successful|Challan Paid)\b', text, re.IGNORECASE))
    pending = bool(re.search(r'\b(PENDING|UNPAID|Due)\b', text, re.IGNORECASE))
    status = "PAID" if paid else ("PENDING" if pending else "UNVERIFIABLE")

    result["verification"] = {
        "employer_code_found": bool(result["extracted"].get("employer_code")),
        "contribution_status": status,
        "esic_verified": paid,
        "source": "PDF_OCR",
        "note": "In production: verify via ESIC portal with employer code for live compliance status."
    }

    return result


def parse_startup(pdf_bytes: bytes) -> dict:
    """Parse DPIIT/Startup India recognition certificate PDF."""
    text = _extract_text(pdf_bytes)
    result = {
        "document_type": "STARTUP_INDIA_RECOGNITION",
        "extracted": {},
        "verification": {},
        "source": "PDF_OCR"
    }

    # Recognition number (DIPP/DPIIT prefix)
    m = re.search(r'(DIPP\d+|DPIIT\d+|[A-Z]{4,}\d{4,})', text)
    if m:
        result["extracted"]["recognition_number"] = m.group(1)

    # Entity name
    m = re.search(r'(?:Name of Entity|Name of Startup|Company Name)[:\s]+([A-Z][A-Za-z\s&\.]+?)(?=\n|PAN|Recognition)', text, re.IGNORECASE)
    if m:
        result["extracted"]["entity_name"] = m.group(1).strip()

    # Recognition date
    m = re.search(r'(?:Date of Recognition|Recognized on|Recognition Date)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4}|\d{1,2}\s+[A-Za-z]+\s+\d{4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["recognition_date"] = m.group(1).strip()

    # Validity
    m = re.search(r'(?:Valid Till|Validity|Valid Until)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4}|\d{1,2}\s+[A-Za-z]+\s+\d{4}|Lifetime|Perpetual)', text, re.IGNORECASE)
    if m:
        result["extracted"]["validity"] = m.group(1).strip()

    # Certificate status
    active = bool(re.search(r'\b(Active|Valid|Recognized|Certified)\b', text, re.IGNORECASE))
    result["extracted"]["certificate_status"] = "ACTIVE" if active else "INACTIVE"

    recog_num_found = bool(result["extracted"].get("recognition_number"))
    result["verification"] = {
        "recognition_number_found": recog_num_found,
        "certificate_active": active and recog_num_found,
        "emd_exemption_supported": active and recog_num_found,  # Startups may claim EMD exemption
        "source": "PDF_OCR",
        "note": "EMD exemption claim requires tender-specific eligibility check. Certificate validity does not automatically guarantee exemption for all tenders."
    }

    return result


def parse_nsic(pdf_bytes: bytes) -> dict:
    """Parse NSIC (National Small Industries Corporation) registration certificate PDF."""
    text = _extract_text(pdf_bytes)
    result = {
        "document_type": "NSIC_REGISTRATION_CERTIFICATE",
        "extracted": {},
        "verification": {},
        "source": "PDF_OCR"
    }

    # Certificate number
    m = re.search(r'(?:Certificate No|Registration No|NSIC No)[:\s]*([A-Z0-9/\-]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["certificate_number"] = m.group(1).strip()

    # Enterprise name
    m = re.search(r'(?:Name of Enterprise|Name of Unit|Firm Name)[:\s]+([A-Z][A-Za-z\s&\.]+?)(?=\n|Address|Registration)', text, re.IGNORECASE)
    if m:
        result["extracted"]["enterprise_name"] = m.group(1).strip()

    # Issue date
    m = re.search(r'(?:Date of Issue|Issue Date|Issued on)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["issue_date"] = m.group(1).strip()

    # Validity
    m = re.search(r'(?:Valid Till|Valid Upto|Validity)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["validity"] = m.group(1).strip()

    # Category
    m = re.search(r'(?:Category|Class)[:\s]*([A-Za-z\s\-IV]+?)(?=\n|\d)', text, re.IGNORECASE)
    if m:
        result["extracted"]["category"] = m.group(1).strip()

    cert_found = bool(result["extracted"].get("certificate_number"))
    result["verification"] = {
        "certificate_number_found": cert_found,
        "nsic_valid": cert_found,
        "emd_exemption_supported": cert_found,  # NSIC-registered MSEs claim EMD exemption
        "source": "PDF_OCR",
        "note": "NSIC registration provides EMD exemption eligibility. Verify currency of certificate before awarding exemption."
    }

    return result


def parse_work_order(pdf_bytes: bytes) -> dict:
    """Parse Work Order / Purchase Order / Contract PDF. Extracts value, dates, parties."""
    text = _extract_text(pdf_bytes)
    result = {
        "document_type": "WORK_ORDER",
        "extracted": {},
        "verification": {},
        "source": "PDF_OCR"
    }

    # Client / Buyer
    m = re.search(r'(?:Client|Buyer|Issued by|To|From)[:\s]+([A-Z][A-Za-z\s&\.]+(?:Ltd|Limited|Corporation|Corp|Industries|ONGC|HPCL|BPCL|CPCL|Reliance|Tata))', text, re.IGNORECASE)
    if m:
        result["extracted"]["client"] = m.group(1).strip()

    # Vendor / Contractor
    m = re.search(r'(?:Vendor|Contractor|Supplier|To M/s|Dear M/s)[:\s]+([A-Z][A-Za-z\s&\.]+(?:Ltd|Limited|Pvt|Private|LLP|Services)?)', text, re.IGNORECASE)
    if m:
        result["extracted"]["vendor"] = m.group(1).strip()

    # Work Order Number
    m = re.search(r'(?:Work Order No|WO No|PO No|Order No|Reference No)[:\s.]*([A-Z0-9/\-]+)', text, re.IGNORECASE)
    if m:
        result["extracted"]["wo_number"] = m.group(1).strip()

    # Order Date
    m = re.search(r'(?:Order Date|Date of Order|Dated|Issue Date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s+[A-Za-z]+\s+\d{4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["order_date"] = m.group(1).strip()

    # Project description / scope
    m = re.search(r'(?:Subject|Re:|Description|Scope)[:\s]+([A-Za-z][A-Za-z\s,\-\.]{10,120})', text, re.IGNORECASE)
    if m:
        result["extracted"]["project_description"] = m.group(1).strip()[:200]

    # Order Value — look for ₹ or Rs. followed by number
    value_found = False
    # Try crore pattern first
    m = re.search(r'(?:Order Value|Contract Value|PO Value|Amount|Total)[^\d]*(?:Rs\.?|INR|₹)[\s\.]*(\d[\d,\.]+)\s*(?:Crore|Cr\.?|crores?)', text, re.IGNORECASE)
    if m:
        raw = m.group(1).replace(',', '')
        result["extracted"]["order_value_cr"] = float(raw)
        result["extracted"]["currency"] = "INR"
        value_found = True
    else:
        # Try lakh pattern
        m = re.search(r'(?:Order Value|Contract Value|PO Value|Amount|Total)[^\d]*(?:Rs\.?|INR|₹)[\s\.]*(\d[\d,\.]+)\s*(?:Lakh|Lakhs?|L\.)', text, re.IGNORECASE)
        if m:
            raw = float(m.group(1).replace(',', ''))
            result["extracted"]["order_value_cr"] = round(raw / 100, 4)  # convert lakh to crore
            result["extracted"]["currency"] = "INR"
            value_found = True
        else:
            # Try plain number pattern
            m = re.search(r'(?:Order Value|Contract Value|Total Amount)[^\n]*?(?:Rs\.?|₹)\s*(\d[\d,\.]+)', text, re.IGNORECASE)
            if m:
                raw = float(m.group(1).replace(',', ''))
                # Assume in rupees if very large number
                if raw > 100000:
                    result["extracted"]["order_value_cr"] = round(raw / 10000000, 4)
                else:
                    result["extracted"]["order_value_cr"] = raw
                result["extracted"]["currency"] = "INR"
                value_found = True

    # Completion date
    m = re.search(r'(?:Completion Date|Delivery Date|Date of Completion|Completed on)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s+[A-Za-z]+\s+\d{4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["completion_date"] = m.group(1).strip()

    # Execution status
    completed = bool(re.search(r'\b(Completed|Executed|Delivered|Finished|Closed)\b', text, re.IGNORECASE))
    result["extracted"]["execution_status"] = "COMPLETED" if completed else "IN_PROGRESS_OR_UNKNOWN"

    # Confidence scoring
    fields_found = sum(1 for v in [result["extracted"].get("wo_number"), result["extracted"].get("order_value_cr"), result["extracted"].get("order_date")] if v)
    confidence = fields_found / 3.0

    result["verification"] = {
        "wo_number_found": bool(result["extracted"].get("wo_number")),
        "value_extracted": value_found,
        "date_extracted": bool(result["extracted"].get("order_date")),
        "extraction_confidence": round(confidence, 2),
        "source": "PDF_OCR",
        "note": "Order value treated as executed value only if completion evidence found. Manual review recommended for high-value claims."
    }
    if confidence < 0.5:
        result["verification"]["status"] = "LOW_CONFIDENCE"
        result["verification"]["manual_review_required"] = True

    return result


def parse_turnover_ca(pdf_bytes: bytes) -> dict:
    """Parse CA-certified Turnover Certificate / Audited Balance Sheet. Extracts financial data and UDIN."""
    text = _extract_text(pdf_bytes)
    result = {
        "document_type": "CA_TURNOVER_CERTIFICATE",
        "extracted": {},
        "verification": {},
        "source": "PDF_OCR"
    }

    # Company Name
    m = re.search(r'(?:Company Name|Name of Company|M/s)[:\s]+([A-Z][A-Za-z\s&\.]+(?:Ltd|Limited|Pvt|LLP|Private))', text, re.IGNORECASE)
    if m:
        result["extracted"]["company_name"] = m.group(1).strip()

    # Financial Year
    m = re.search(r'(?:Financial Year|FY|For the year)[:\s]*(\d{4}[-–]\d{2,4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["financial_year"] = m.group(1).strip()

    # Turnover
    m = re.search(r'(?:Annual Turnover|Turnover|Gross Revenue|Net Sales)[^\d]*(?:Rs\.?|INR|₹)[\s\.]*(\d[\d,\.]+)\s*(?:Crore|Cr\.?)', text, re.IGNORECASE)
    if m:
        result["extracted"]["turnover_cr"] = float(m.group(1).replace(',', ''))
    else:
        # Try lakh
        m = re.search(r'(?:Annual Turnover|Turnover)[^\d]*(?:Rs\.?|₹)[\s\.]*(\d[\d,\.]+)\s*(?:Lakh|L)', text, re.IGNORECASE)
        if m:
            result["extracted"]["turnover_cr"] = round(float(m.group(1).replace(',', '')) / 100, 4)

    # CA Name
    m = re.search(r'(?:CA|Chartered Accountant|Name of CA)[:\s]+([A-Z][A-Za-z\s\.]+?)(?=\n|MRN|Membership|UDIN)', text, re.IGNORECASE)
    if m:
        result["extracted"]["ca_name"] = m.group(1).strip()

    # Membership Number
    m = re.search(r'(?:Membership No|MRN|M\.No)[:\s.]*([0-9]{6})', text, re.IGNORECASE)
    if m:
        result["extracted"]["membership_number"] = m.group(1)

    # UDIN — format: YYXXXXXXYYYYYYYYYY (20 chars)
    m = re.search(r'\b(\d{2}[A-Z0-9]{6}[A-Z0-9]{12})\b|UDIN[:\s]*([A-Z0-9]{18,22})', text)
    udin_value = None
    if m:
        udin_value = (m.group(1) or m.group(2))
        result["extracted"]["udin"] = udin_value

    # Certificate Date
    m = re.search(r'(?:Date|Dated|Certificate Date)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text, re.IGNORECASE)
    if m:
        result["extracted"]["certificate_date"] = m.group(1).strip()

    # UDIN validation states (format only — no live ICAI API)
    udin_format_valid = False
    if udin_value:
        udin_format_valid = bool(re.match(r'^\d{2}[A-Z0-9]{6}[A-Z0-9]{12}$', udin_value))

    if udin_value and udin_format_valid:
        udin_state = "UDIN_FORMAT_VALID"
    elif udin_value:
        udin_state = "UDIN_FOUND_FORMAT_INVALID"
    else:
        udin_state = "UDIN_NOT_FOUND"

    result["verification"] = {
        "turnover_extracted": bool(result["extracted"].get("turnover_cr")),
        "ca_name_found": bool(result["extracted"].get("ca_name")),
        "udin_found": bool(udin_value),
        "udin_format_valid": udin_format_valid,
        "udin_verification_state": udin_state,
        "source": "PDF_OCR",
        "note": "Format/document validation completed — external ICAI UDIN verification unavailable in demo mode. Production deployment should call ICAI UDIN verification API.",
        "disclaimer": "This is document-level validation only. It does not constitute official government verification."
    }

    return result
