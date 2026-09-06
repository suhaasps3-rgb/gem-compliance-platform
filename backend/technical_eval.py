"""
technical_eval.py — Technical Specification Evaluation Engine.
Compares tender technical requirements against vendor-submitted specifications.
"""
import re
from typing import List, Dict, Any, Optional
import pymupdf


OPERATOR_SYMBOLS = {
    "gte": ">=", "lte": "<=", "eq": "=",
    "gt": ">", "lt": "<", "between": "between",
    "contains": "contains", "is_true": "is"
}


def _normalize_value(val: Any) -> Optional[float]:
    """Try to extract a numeric value from a string or number."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        m = re.search(r'([\d.]+)', val.replace(',', ''))
        if m:
            return float(m.group(1))
    return None


def evaluate_parameter(
    parameter: str,
    operator: str,          # 'gte', 'lte', 'eq', 'gt', 'lt', 'between', 'contains', 'is_true'
    required_value: Any,
    vendor_value: Any,
    unit: str = "",
    second_required_value: Any = None  # for 'between'
) -> Dict[str, Any]:
    """Evaluate a single technical parameter."""
    try:
        req_num = _normalize_value(required_value)
        ven_num = _normalize_value(vendor_value)

        passed = False
        deviation = None
        comparison_str = ""

        if operator == "gte":
            passed = ven_num is not None and req_num is not None and ven_num >= req_num
            comparison_str = f">= {required_value} {unit}"
            if ven_num is not None and req_num is not None:
                deviation = round(ven_num - req_num, 3)
        elif operator == "lte":
            passed = ven_num is not None and req_num is not None and ven_num <= req_num
            comparison_str = f"<= {required_value} {unit}"
            if ven_num is not None and req_num is not None:
                deviation = round(ven_num - req_num, 3)
        elif operator == "eq":
            if ven_num is not None and req_num is not None:
                passed = abs(ven_num - req_num) < 0.001
                deviation = round(ven_num - req_num, 3)
            else:
                passed = str(vendor_value).strip().lower() == str(required_value).strip().lower()
            comparison_str = f"= {required_value} {unit}"
        elif operator == "between":
            req2_num = _normalize_value(second_required_value)
            if ven_num is not None and req_num is not None and req2_num is not None:
                passed = req_num <= ven_num <= req2_num
            comparison_str = f"between {required_value} and {second_required_value} {unit}"
        elif operator == "contains":
            passed = str(required_value).lower() in str(vendor_value).lower()
            comparison_str = f"contains '{required_value}'"
        elif operator == "is_true":
            passed = bool(vendor_value)
            comparison_str = "= Yes"
        else:
            passed = False
            comparison_str = f"{operator} {required_value}"

        return {
            "parameter": parameter,
            "requirement": f"{comparison_str}",
            "vendor_value": str(vendor_value),
            "unit": unit,
            "operator": OPERATOR_SYMBOLS.get(operator, operator),
            "result": "PASS" if passed else "FAIL",
            "deviation": deviation,
            "passed": passed
        }
    except Exception as e:
        return {
            "parameter": parameter,
            "requirement": str(required_value),
            "vendor_value": str(vendor_value),
            "unit": unit,
            "operator": operator,
            "result": "ERROR",
            "deviation": None,
            "passed": False,
            "error": str(e)
        }


def evaluate_technical_specs(
    tender_specs: List[Dict[str, Any]],
    vendor_specs: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluate vendor technical specs against tender requirements.

    Args:
        tender_specs: List of {parameter, operator, required_value, unit, second_value?}
        vendor_specs: List of {parameter, vendor_value}

    Returns:
        Full evaluation matrix with per-parameter results and summary
    """
    # Build vendor lookup
    vendor_lookup = {spec["parameter"].lower(): spec["vendor_value"] for spec in vendor_specs}

    matrix = []
    pass_count = 0
    fail_count = 0
    missing_count = 0

    for spec in tender_specs:
        param = spec["parameter"]
        param_lower = param.lower()
        vendor_val = vendor_lookup.get(param_lower)

        if vendor_val is None:
            matrix.append({
                "parameter": param,
                "requirement": f"{OPERATOR_SYMBOLS.get(spec['operator'], spec['operator'])} {spec['required_value']} {spec.get('unit', '')}",
                "vendor_value": "NOT PROVIDED",
                "unit": spec.get("unit", ""),
                "operator": OPERATOR_SYMBOLS.get(spec['operator'], spec['operator']),
                "result": "MISSING",
                "deviation": None,
                "passed": False
            })
            missing_count += 1
            continue

        row = evaluate_parameter(
            parameter=param,
            operator=spec["operator"],
            required_value=spec["required_value"],
            vendor_value=vendor_val,
            unit=spec.get("unit", ""),
            second_required_value=spec.get("second_required_value")
        )
        matrix.append(row)
        if row["result"] == "PASS":
            pass_count += 1
        else:
            fail_count += 1

    total = len(tender_specs)
    tech_score = round((pass_count / total * 100) if total > 0 else 0, 1)
    overall = "PASS" if fail_count == 0 and missing_count == 0 else ("FAIL" if fail_count > 0 else "INCOMPLETE")

    return {
        "overall_result": overall,
        "technical_score": tech_score,
        "parameters_evaluated": total,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "missing_count": missing_count,
        "matrix": matrix,
        "summary": f"{pass_count}/{total} parameters pass technical requirements."
    }


def extract_specs_from_pdf(pdf_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Attempt to extract technical spec values from a vendor catalog/datasheet PDF.
    Returns a list of {parameter, vendor_value} dicts.
    """
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        text = " ".join(page.get_text() for page in doc)
    except Exception:
        return []

    specs = []
    # Pump capacity
    m = re.search(r'(?:Pump Capacity|Flow Rate|Capacity)[:\s]*(\d+[\d.]*)\s*m[\u00b3³]?/hr', text, re.IGNORECASE)
    if m: specs.append({"parameter": "Pump Capacity", "vendor_value": float(m.group(1))})

    # Pressure
    m = re.search(r'(?:Discharge Pressure|Operating Pressure|Pressure)[:\s]*(\d+[\d.]*)\s*(?:bar|Bar|BAR)', text, re.IGNORECASE)
    if m: specs.append({"parameter": "Pressure", "vendor_value": float(m.group(1))})

    # Efficiency
    m = re.search(r'(?:Pump Efficiency|Efficiency)[:\s]*(\d+[\d.]*)\s*%', text, re.IGNORECASE)
    if m: specs.append({"parameter": "Efficiency", "vendor_value": float(m.group(1))})

    # Voltage
    m = re.search(r'(?:Supply Voltage|Voltage|Power Supply)[:\s]*(\d+)\s*V', text, re.IGNORECASE)
    if m: specs.append({"parameter": "Voltage", "vendor_value": int(m.group(1))})

    # Motor Power
    m = re.search(r'(?:Motor Power|Power Rating)[:\s]*(\d+[\d.]*)\s*(?:kW|KW)', text, re.IGNORECASE)
    if m: specs.append({"parameter": "Motor Power", "vendor_value": float(m.group(1))})

    # Material
    m = re.search(r'(?:Casing Material|Impeller Material|Material)[:\s]+([A-Za-z\s\-]+?)(?=\n|,|\.|\d)', text, re.IGNORECASE)
    if m: specs.append({"parameter": "Casing Material", "vendor_value": m.group(1).strip()})

    return specs
