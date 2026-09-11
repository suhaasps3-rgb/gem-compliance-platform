import json

with open("database/mock_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for b in data["bidders"]:
    if b["id"] == "bidder-beta-002":
        # Fix contradictions - Beta should fail due to Turnover and Subcontracting, not MII
        b["active_contradictions"] = [
            {"issue": "Turnover 18.0 Cr exceeds MSME cap of 15 Cr", "source": "Turnover_Certificate"},
            {"issue": "Sub-contracting 15% exceeds allowed cap of 10%", "source": "Bid_Document"}
        ]
        # Fix submitted docs - ensure MII is listed as submitted
        b["claims"]["submitted_docs"] = [
            "GST_Certificate",
            "PAN_Card",
            "Turnover_Certificate",
            "Local_Content_Declaration",
            "Udyam_Certificate"
        ]
        # Fix AI recommendation
        b["ai_recommendation"] = {
            "decision": "NEEDS REVIEW",
            "missing_docs": [],
            "reasoning": "Turnover of INR 18.0 Cr exceeds the MSME eligibility cap of INR 15 Cr. Additionally, sub-contracting percentage of 15% breaches the 10% tender cap. Requires clarification.",
            "red_flags": [
                "Turnover 18.0 Cr exceeds MSME cap (15 Cr)",
                "Sub-contracting 15% exceeds tender cap (10%)"
            ]
        }
        print("Beta LLC patched.")
        break

with open("database/mock_dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saved.")
