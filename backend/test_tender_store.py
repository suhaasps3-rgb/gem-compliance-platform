"""Tests for the persisted tender model and the closing-date logic. Run: python test_tender_store.py"""
import json
import os
import tempfile

_tmp = tempfile.mkdtemp()
os.environ["SATARK_TENDER_STORE"] = os.path.join(_tmp, "tenders.json")

import tender_store
from graph_engine import EvidenceGraphEngine
from technical_eval import evaluate_technical_specs

MOCK = os.path.join(os.path.dirname(__file__), "..", "database", "mock_dataset.json")


def _bidders():
    with open(MOCK, "r", encoding="utf-8") as f:
        return {b["id"]: b for b in json.load(f)["bidders"]}


def test_default_tender_keeps_previous_closing_date():
    assert tender_store.get_closing_date() == "2025-12-01"
    assert tender_store.get_tender("tender-sih-2026")["criteria"]["min_experience_cr"] == 5.0


def test_upsert_persists_to_disk_and_reloads():
    rec = tender_store.upsert_tender({
        "id": "tender-test-1", "title": "T1", "closing_date": "2026-03-31",
        "criteria": {"min_turnover_cr": 7}, "required_documents": ["GST_Certificate"],
    })
    assert rec["closing_date"] == "2026-03-31"
    with open(os.environ["SATARK_TENDER_STORE"], encoding="utf-8") as f:
        on_disk = json.load(f)
    assert "tender-test-1" in on_disk
    assert tender_store.get_tender("tender-test-1")["criteria"]["min_turnover_cr"] == 7
    assert any(t["id"] == "tender-test-1" for t in tender_store.list_tenders())


def test_bad_input_is_rejected():
    for bad in ("2026-13-45", "31/03/2026", "", None, 20260331):
        try:
            tender_store.upsert_tender({"id": "x1", "closing_date": bad})
        except ValueError:
            continue
        raise AssertionError(f"accepted bad closing_date {bad!r}")
    for bad_id in ("", "../etc", "a b", "x" * 65, None):
        try:
            tender_store.upsert_tender({"id": bad_id, "closing_date": "2026-01-01"})
        except ValueError:
            continue
        raise AssertionError(f"accepted bad id {bad_id!r}")


def test_unknown_tender_falls_back_to_default_date():
    assert tender_store.get_tender("nope") is None
    assert tender_store.get_closing_date("nope") == "2025-12-01"


def test_debarment_is_judged_as_of_the_tenders_closing_date():
    bidders = _bidders()
    theta = next((b for b in bidders.values()
                  if b.get("debarment_mock", {}).get("historical_records")), None)
    assert theta, "mock data should contain a bidder with historical debarment"
    rec = theta["debarment_mock"]["historical_records"][0]

    inside = rec["start_date"]
    outside = "1999-01-01"
    for closing, expect_conflict in ((inside, True), (outside, False)):
        e = EvidenceGraphEngine(theta, tender_closing_date=closing)
        e.build_graph()
        ids = [c["contradiction_id"] for c in e.resolve_contradictions()["contradictions"]]
        assert any("debarment" in i for i in ids) == expect_conflict, (closing, ids)


def test_engine_reads_closing_date_from_the_stored_tender():
    tender_store.upsert_tender({"id": "tender-test-2", "closing_date": "2024-02-02"})
    e = EvidenceGraphEngine(next(iter(_bidders().values())), tender_id="tender-test-2")
    assert e.tender_closing_date == "2024-02-02"


def test_no_extracted_specs_is_incomplete_never_pass():
    specs = [{"parameter": "Pressure", "operator": "gte", "required_value": 20, "unit": "bar"}]
    res = evaluate_technical_specs(specs, [])
    assert res["overall_result"] == "INCOMPLETE"
    assert res["matrix"][0]["result"] == "MISSING"
    assert res["matrix"][0]["passed"] is False


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print(f"{len(tests)} passed")
