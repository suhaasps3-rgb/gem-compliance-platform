import os
import json

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance'
f = os.path.join(ROOT, 'database', 'mock_dataset.json')

with open(f, 'r', encoding='utf-8') as file:
    data = json.load(file)

bidders = data.get("bidders", [])

for b in bidders:
    bid = b.get("id")
    # Add submission IP to all bidders
    if "submission_metadata" not in b:
        b["submission_metadata"] = {}
    if bid == "bidder-acme-001":
        b["epfo_mock"] = {"status": "ACTIVE", "employee_count": 22, "contribution_period": "August 2026", "contribution_status": "PAID"}
        b["esic_mock"] = {"status": "ACTIVE", "contribution_status": "PAID"}
        b["startup_mock"] = None
        b["nsic_mock"] = None
        b["work_orders"] = [
            {"wo_number": "WO-1023", "client": "Reliance Industries", "value_cr": 2.10, "order_date": "01/04/2023", "fy": "2023-24", "confidence": 0.94},
            {"wo_number": "WO-1187", "client": "ONGC", "value_cr": 1.75, "order_date": "15/09/2022", "fy": "2022-23", "confidence": 0.88},
            {"wo_number": "WO-1452", "client": "HPCL", "value_cr": 3.50, "order_date": "10/12/2024", "fy": "2024-25", "confidence": 0.91}
        ]
        b["technical_specs"] = {"Pump Capacity": 520, "Pressure": 22, "Efficiency": 91, "Voltage": 415}
        b["submission_metadata"]["ip_address"] = "10.0.1.5"
        b["submission_metadata"]["user_agent"] = "Chrome/126"
    elif bid == "bidder-delta-004":
        b["submission_metadata"]["ip_address"] = "10.0.1.5"
    elif bid == "bidder-foxtrot-006":
        b["work_orders"] = [
            {"wo_number": "WO-0987", "client": "Indian Oil", "value_cr": 1.20, "order_date": "01/06/2021", "fy": "2021-22", "confidence": 0.82}
        ]
        b["technical_specs"] = {"Pump Capacity": 450, "Pressure": 18, "Efficiency": 87, "Voltage": 415}
        b["submission_metadata"]["ip_address"] = "192.168.5.22"
    else:
        if "ip_address" not in b["submission_metadata"]:
            b["submission_metadata"]["ip_address"] = "192.168.1." + str(hash(bid) % 255)

# Add 3 new bidders if not already there
existing_ids = [b["id"] for b in bidders]
if "bidder-indigo-010" not in existing_ids:
    bidders.extend([
        {
          "id": "bidder-indigo-010",
          "name": "Indigo Innovations Pvt Ltd",
          "scenario": "Startup India + NSIC Exemptions",
          "expected_status": "VERIFIED_COMPLIANT",
          "claims": {"turnover_cr": 3.2, "local_content_pct": 65, "subcontracting_pct": 10, "pan": "INDGO9012P", "is_msme": True},
          "mca21_mock": {"reported_turnover_cr": 3.2, "active_directors": ["DIN55556666"]},
          "udyam_mock": {"status": "ACTIVE", "enterprise_type": "Micro"},
          "gst_mock": {"status": "ACTIVE"},
          "gstn_mock": {"status": "ACTIVE", "gstr_filed_continuous_12m": True, "months_missed": 0},
          "startup_mock": {"recognition_number": "DIPP12345", "certificate_status": "ACTIVE", "entity_name": "Indigo Innovations Pvt Ltd", "emd_exemption_supported": True},
          "nsic_mock": {"certificate_number": "NS/MC/CH/2023/01234", "nsic_valid": True, "emd_exemption_supported": True},
          "work_orders": [{"wo_number": "WO-2201", "client": "BPCL", "value_cr": 6.80, "order_date": "20/07/2023", "fy": "2023-24", "confidence": 0.92}],
          "technical_specs": {"Pump Capacity": 510, "Pressure": 21, "Efficiency": 92, "Voltage": 415},
          "submission_metadata": {"ip_address": "172.16.0.10"}
        },
        {
          "id": "bidder-juliet-011",
          "name": "Juliet Engineering Works",
          "scenario": "Turnover UDIN Validation",
          "expected_status": "NEEDS_REVIEW",
          "claims": {"turnover_cr": 8.5, "local_content_pct": 60, "subcontracting_pct": 12, "pan": "JULET4567K", "is_msme": True},
          "mca21_mock": {"reported_turnover_cr": 8.5, "active_directors": ["DIN77778888"]},
          "udyam_mock": {"status": "ACTIVE", "enterprise_type": "Micro"},
          "gst_mock": {"status": "ACTIVE"},
          "gstn_mock": {"status": "ACTIVE", "gstr_filed_continuous_12m": True, "months_missed": 0},
          "ca_certificate_mock": {"financial_year": "2024-25", "turnover_cr": 8.5, "ca_name": "CA Ramesh Kumar", "udin": "24333ABC123456", "udin_format_valid": True, "udin_verification_state": "UDIN_FORMAT_VALID"},
          "submission_metadata": {"ip_address": "172.16.0.10"}
        },
        {
          "id": "bidder-kilo-012",
          "name": "Kilo Systems Ltd",
          "scenario": "Technical Specs FAIL",
          "expected_status": "NEEDS_REVIEW",
          "claims": {"turnover_cr": 6.0, "local_content_pct": 55, "subcontracting_pct": 18, "pan": "KILOS6789M", "is_msme": True},
          "mca21_mock": {"reported_turnover_cr": 6.0, "active_directors": ["DIN99990000"]},
          "udyam_mock": {"status": "ACTIVE", "enterprise_type": "Micro"},
          "gst_mock": {"status": "ACTIVE"},
          "gstn_mock": {"status": "ACTIVE", "gstr_filed_continuous_12m": True, "months_missed": 0},
          "technical_specs": {"Pump Capacity": 450, "Pressure": 18, "Efficiency": 87, "Voltage": 415},
          "submission_metadata": {"ip_address": "203.0.113.55"}
        }
    ])

with open(f, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2)

print('Mock dataset updated.')
