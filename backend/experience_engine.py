"""
experience_engine.py — Work Order Experience Aggregation and Validation Engine.
Validates whether a bidder's past work orders meet the minimum experience requirement.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional


def _parse_date(date_str: str) -> Optional[datetime]:
    """Try parsing common date formats."""
    if not date_str:
        return None
    for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%d %B %Y", "%B %d, %Y", "%Y-%m-%d"]:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def _date_to_financial_year(dt: datetime) -> str:
    """Convert a date to its financial year string (e.g., '2023-24')."""
    if dt.month >= 4:  # April onwards = current FY
        return f"{dt.year}-{str(dt.year + 1)[-2:]}"
    else:
        return f"{dt.year - 1}-{str(dt.year)[-2:]}"


def _eligible_fy_range(eligible_years: int = 5) -> tuple:
    """Return the start and end financial years for the eligible period."""
    current = datetime.now()
    current_fy_start = current.year if current.month >= 4 else current.year - 1
    start_fy = current_fy_start - eligible_years
    return start_fy, current_fy_start


def validate_experience(
    work_orders: List[Dict[str, Any]],
    requirement_cr: float,
    eligible_years: int = 5
) -> Dict[str, Any]:
    """
    Validates bidder past experience against a minimum requirement.

    Args:
        work_orders: List of parse_work_order() results
        requirement_cr: Minimum required experience in Crores
        eligible_years: Look-back window in years (default 5)

    Returns:
        result dict with PASS/FAIL/INSUFFICIENT_EVIDENCE, evidence list, and total eligible value
    """
    fy_start, fy_end = _eligible_fy_range(eligible_years)
    eligible_period_str = f"FY {fy_start}-{str(fy_start+1)[-2:]} to FY {fy_end}-{str(fy_end+1)[-2:]}"

    eligible_wos = []
    excluded_wos = []
    seen_wo_numbers = set()  # deduplication
    total_eligible_cr = 0.0
    has_any_value = False

    for wo_result in work_orders:
        extracted = wo_result.get("extracted", {})
        verification = wo_result.get("verification", {})

        wo_number = extracted.get("wo_number", "UNKNOWN")
        value_cr = extracted.get("order_value_cr")
        order_date_str = extracted.get("order_date") or extracted.get("completion_date", "")
        value_extracted = verification.get("value_extracted", False)
        confidence = verification.get("extraction_confidence", 0)

        if value_cr is not None:
            has_any_value = True

        # Skip if no value extracted
        if not value_extracted or value_cr is None:
            excluded_wos.append({
                "wo_number": wo_number,
                "reason": "Order value could not be extracted from document",
                "confidence": confidence
            })
            continue

        # Deduplication
        if wo_number != "UNKNOWN" and wo_number in seen_wo_numbers:
            excluded_wos.append({
                "wo_number": wo_number,
                "reason": "Duplicate work order — already counted",
                "value_cr": value_cr
            })
            continue

        # Date eligibility
        order_dt = _parse_date(order_date_str)
        fy = None
        in_window = True  # Include if we can't determine date

        if order_dt:
            fy = _date_to_financial_year(order_dt)
            fy_year = int(fy.split("-")[0])
            in_window = fy_start <= fy_year <= fy_end

        if not in_window:
            excluded_wos.append({
                "wo_number": wo_number,
                "reason": f"Work order date {order_date_str} falls outside eligible period ({eligible_period_str})",
                "value_cr": value_cr,
                "fy": fy
            })
            continue

        # Eligible!
        seen_wo_numbers.add(wo_number)
        total_eligible_cr += value_cr
        eligible_wos.append({
            "wo_number": wo_number,
            "value_cr": round(value_cr, 2),
            "client": extracted.get("client", "Not extracted"),
            "order_date": order_date_str,
            "fy": fy or "Date not extracted",
            "confidence": confidence,
            "execution_status": extracted.get("execution_status", "UNKNOWN")
        })

    total_eligible_cr = round(total_eligible_cr, 2)

    # Determine result
    if not has_any_value and not eligible_wos:
        result_status = "INSUFFICIENT_EVIDENCE"
        result_note = "No work order values could be extracted from the provided documents. Manual review required."
    elif total_eligible_cr >= requirement_cr:
        result_status = "PASS"
        result_note = f"Eligible experience of ₹{total_eligible_cr} Cr meets the requirement of ₹{requirement_cr} Cr."
    else:
        result_status = "FAIL"
        result_note = f"Eligible experience of ₹{total_eligible_cr} Cr falls short of the ₹{requirement_cr} Cr requirement by ₹{round(requirement_cr - total_eligible_cr, 2)} Cr."

    return {
        "result": result_status,
        "requirement_cr": requirement_cr,
        "eligible_cr": total_eligible_cr,
        "shortfall_cr": max(0, round(requirement_cr - total_eligible_cr, 2)),
        "eligible_period": eligible_period_str,
        "work_orders_submitted": len(work_orders),
        "work_orders_eligible": len(eligible_wos),
        "work_orders_excluded": len(excluded_wos),
        "evidence": eligible_wos,
        "excluded": excluded_wos,
        "note": result_note,
        "disclaimer": "Work order value is treated as executed value only where document evidence supports it. Unverified values require manual review."
    }
