import json

with open(r'database\mock_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for bidder in data['bidders']:
    if bidder['id'] == 'bidder-acme-001':
        bidder['scenario'] = 'Green (Compliant)'
        bidder['expected_status'] = 'VERIFIED_COMPLIANT'
        bidder['ai_recommendation'] = {
            'decision': 'RECOMMENDED',
            'reasoning': 'All extracted claims match statutory registry evidence perfectly. AI confirms Udyam, ITR, and MCA21 data reconcile.',
            'red_flags': [],
            'missing_docs': []
        }
    elif bidder['id'] == 'bidder-beta-002':
        bidder['scenario'] = 'Yellow (Clarification Needed)'
        bidder['expected_status'] = 'NEEDS_REVIEW'
        bidder['ai_recommendation'] = {
            'decision': 'NEEDS REVIEW',
            'reasoning': 'Bidder claimed Make-in-India Class-I exemption, but the uploaded MII document does not specify the local content percentage.',
            'red_flags': ['MII Declaration missing explicit Local Content %'],
            'missing_docs': ['Local_Content_Declaration']
        }
        bidder['active_contradictions'] = [{'source': 'MII_Declaration', 'issue': 'Missing Local Content %'}]
    elif bidder['id'] == 'bidder-gamma-003':
        bidder['scenario'] = 'Red (Critical Fraud)'
        bidder['expected_status'] = 'NON_COMPLIANT'
        bidder['ai_recommendation'] = {
            'decision': 'NOT RECOMMENDED',
            'reasoning': 'CRITICAL FRAUD: Identity anchoring failed. The PAN extracted from the uploaded ITR belongs to a different entity. Furthermore, temporal evaluation found an active debarment on the tender closing date.',
            'red_flags': ['Cross-Bidder Forgery: Extracted PAN (REAL9999X) != Registered PAN (BKKPA1234F)', 'Active Debarment found in MoF Registry'],
            'missing_docs': []
        }
        bidder['debarment_mock'] = {
            "historical_records": [
                {"start_date": "2023-01-01", "end_date": "2026-01-01", "reason": "Fraudulent Bid"}
            ]
        }
        bidder['claims']['pan'] = 'BKKPA1234F'
        bidder['itr_mock'] = {
            "status": "FILED",
            "pan": "REAL9999X"
        }
        bidder['active_contradictions'] = [
            {'source': 'Identity', 'issue': 'PAN Mismatch (Forgery)'},
            {'source': 'Debarment', 'issue': 'Active Debarment Found'}
        ]

with open(r'database\mock_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
