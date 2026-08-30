import json
import os
from graph_engine import EvidenceGraphEngine

MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "mock_dataset.json")

def load_mock_data():
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_graph_resolution():
    mock_data = load_mock_data()
    bidders = {b["id"]: b for b in mock_data.get("bidders", [])}

    # Test Delta Solutions (Should have 1 contradiction for Turnover)
    delta_engine = EvidenceGraphEngine(bidders["bidder-delta-004"])
    delta_engine.build_graph()
    delta_results = delta_engine.resolve_contradictions()
    
    assert delta_results["status"] == "NEEDS_REVIEW", f"Expected NEEDS_REVIEW, got {delta_results['status']}"
    assert len(delta_results["contradictions"]) == 1, "Expected 1 contradiction for Delta"
    assert "conflict-turnover" in delta_results["contradictions"][0]["contradiction_id"]
    print("✅ Delta Solutions case (Turnover contradiction) passed.")

    # Test Acme Corp (Should have 0 contradictions)
    acme_engine = EvidenceGraphEngine(bidders["bidder-acme-001"])
    acme_engine.build_graph()
    acme_results = acme_engine.resolve_contradictions()

    assert acme_results["status"] == "VERIFIED_COMPLIANT", f"Expected VERIFIED_COMPLIANT, got {acme_results['status']}"
    assert len(acme_results["contradictions"]) == 0, "Expected 0 contradictions for Acme"
    print("✅ Acme Corp case (Baseline Green) passed.")

    # Test Gamma Technologies (Should have 1 contradiction for Entity Mismatch)
    gamma_engine = EvidenceGraphEngine(bidders["bidder-gamma-003"])
    gamma_engine.build_graph()
    gamma_results = gamma_engine.resolve_contradictions()

    assert gamma_results["status"] == "NEEDS_REVIEW", f"Expected NEEDS_REVIEW, got {gamma_results['status']}"
    assert len(gamma_results["contradictions"]) == 1, "Expected 1 contradiction for Gamma"
    assert "conflict-name" in gamma_results["contradictions"][0]["contradiction_id"]
    print("✅ Gamma Technologies case (Identity Mismatch) passed.")

if __name__ == "__main__":
    test_graph_resolution()
