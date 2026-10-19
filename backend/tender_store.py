"""
tender_store.py — a small persisted tender record.

Each tender carries its own closing date and criteria, so date checks (debarment in force on
the closing date, document validity) are evaluated as of that tender, not as of today or a
hard-coded constant. Stored as JSON so it survives a restart without a database; swap the
two _load/_save functions for a real database later.
"""
import json
import os
import re
import tempfile
import threading
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional

DEFAULT_TENDER_ID = "tender-sih-2026"

_DEFAULT_TENDERS = {
    DEFAULT_TENDER_ID: {
        "id": DEFAULT_TENDER_ID,
        "title": "CPCL high-pressure pumps (demo tender)",
        # Same date the engine used before it was configurable.
        "closing_date": "2025-12-01",
        "criteria": {
            "min_turnover_cr": 10.0,
            "min_experience_cr": 5.0,
            "msme_turnover_cap_cr": 15.0,
            "min_local_content_pct": 60,
            "max_subcontracting_pct": 10,
        },
        "required_documents": [
            "GST_Certificate", "PAN_Card", "Turnover_Certificate",
            "OEM_Authorization", "Local_Content_Declaration",
        ],
    }
}

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_lock = threading.Lock()


def _path() -> str:
    return os.environ.get(
        "SATARK_TENDER_STORE",
        os.path.join(os.path.dirname(__file__), "data", "tenders.json"),
    )


def _load() -> Dict[str, Dict[str, Any]]:
    try:
        with open(_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(tenders: Dict[str, Dict[str, Any]]) -> None:
    path = _path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Write to a temp file and rename so a crash never leaves half a file.
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(tenders, f, indent=2, sort_keys=True)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def validate_closing_date(value: Any) -> str:
    """Return an ISO date string (YYYY-MM-DD) or raise ValueError."""
    if not isinstance(value, str):
        raise ValueError("closing_date must be a YYYY-MM-DD string")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise ValueError("closing_date must be a valid YYYY-MM-DD date")


def list_tenders() -> List[Dict[str, Any]]:
    with _lock:
        merged = {**_DEFAULT_TENDERS, **_load()}
    return [merged[k] for k in sorted(merged)]


def get_tender(tender_id: str) -> Optional[Dict[str, Any]]:
    with _lock:
        stored = _load()
    return stored.get(tender_id) or _DEFAULT_TENDERS.get(tender_id)


def upsert_tender(tender: Dict[str, Any]) -> Dict[str, Any]:
    """Create or update a tender. Raises ValueError on bad input."""
    tender_id = tender.get("id")
    if not isinstance(tender_id, str) or not _ID_RE.match(tender_id):
        raise ValueError("id must be 1-64 letters, digits, dot, dash or underscore")
    record = {
        "id": tender_id,
        "title": str(tender.get("title") or tender_id)[:200],
        "closing_date": validate_closing_date(tender.get("closing_date")),
        "criteria": dict(tender.get("criteria") or {}),
        "required_documents": [str(d) for d in (tender.get("required_documents") or [])],
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with _lock:
        stored = _load()
        stored[tender_id] = record
        _save(stored)
    return record


def get_closing_date(tender_id: str = DEFAULT_TENDER_ID) -> str:
    """Closing date for a tender; falls back to the default demo tender for unknown ids."""
    t = get_tender(tender_id) or _DEFAULT_TENDERS[DEFAULT_TENDER_ID]
    return t["closing_date"]
