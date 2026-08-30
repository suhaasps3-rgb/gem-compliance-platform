import json
import os
from collusion_engine import CollusionEngine

MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "mock_dataset.json")

def load_mock_data():
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_collusion_engine():
    mock_data = load_mock_data()
    bidders = mock_data.get("bidders", [])

    engine = CollusionEngine(bidders)
    results = engine.analyze_collusion("tender-sih-2026")

    assert results["status"] == "ANALYSIS_COMPLETE", "Status should be ANALYSIS_COMPLETE"
    
    leads = results["investigative_leads"]
    
    # We expect exactly 1 lead between Epsilon and Zeta
    assert len(leads) == 1, f"Expected 1 investigative lead, got {len(leads)}"
    
    lead = leads[0]
    assert "bidder-epsilon-005" in lead["bidders_involved"]
    assert "bidder-zeta-006" in lead["bidders_involved"]
    assert "SHARED_DIRECTOR_AND_SHARED_METADATA" == lead["lead_type"]
    assert len(lead["evidence"]) == 2
    assert "heuristic signal" in lead["disclaimer"]

    print("PASS: Cross-Bidder Collusion Engine tests passed. Epsilon/Zeta Wow Case caught successfully.")

if __name__ == "__main__":
    test_collusion_engine()
