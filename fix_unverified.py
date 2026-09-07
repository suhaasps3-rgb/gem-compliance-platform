import json
import re

with open(r'database\mock_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for bidder in data['bidders']:
    if 'gst_mock' not in bidder:
        bidder['gst_mock'] = {}
    bidder['gst_mock']['return_filing_status'] = 'FILED'

with open(r'database\mock_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

with open(r'backend\graph_engine.py', 'r', encoding='utf-8') as f:
    engine = f.read()

engine = engine.replace('"debarment_status": "CLEAR",', '"debarment_status": "PASS",')
engine = engine.replace('self.hard_filters["debarment_status"] = "BLACKLISTED"', 'self.hard_filters["debarment_status"] = "FAIL"')

with open(r'backend\graph_engine.py', 'w', encoding='utf-8') as f:
    f.write(engine)
