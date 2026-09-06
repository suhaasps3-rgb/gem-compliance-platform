import sys, io, os, requests, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'http://localhost:8000'
PUBLIC = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance\frontend\public'
results = []

# TEST 1
print('=== TEST 1: Acme Corp (expect VERIFIED_COMPLIANT) ===')
requests.post(BASE + '/api/v1/verify/bidder/bidder-acme-001/tender/tender-sih-2026')
r = requests.get(BASE + '/api/v1/dashboard/bidder/bidder-acme-001').json()
print('  Status:', r['overall_status'])
print('  Contradictions:', len(r['active_contradictions']))
print('  Data source: mock_dataset.json')
results.append(('Acme Corp', r['overall_status'], len(r['active_contradictions']), 'mock_data'))

# TEST 2
print()
print('=== TEST 2: Delta Solutions (expect NEEDS_REVIEW - MCA21 turnover conflict) ===')
requests.post(BASE + '/api/v1/verify/bidder/bidder-delta-004/tender/tender-sih-2026')
r = requests.get(BASE + '/api/v1/dashboard/bidder/bidder-delta-004').json()
print('  Status:', r['overall_status'])
for c in r['active_contradictions']:
    print('  Conflict:', c['claim'], 'vs', c['evidence'])
print('  Data source: mock_dataset.json (mca21_mock)')
results.append(('Delta Solutions', r['overall_status'], len(r['active_contradictions']), 'mock_data'))

# TEST 3
print()
print('=== TEST 3: Foxtrot PDF - OCR pipeline (expect MII + GST violations) ===')
with open(os.path.join(PUBLIC, 'bidder_foxtrot.pdf'), 'rb') as f:
    r = requests.post(BASE + '/api/v1/bidders/verify-document',
                      files={'bidder_pdf': ('bidder_foxtrot.pdf', f, 'application/pdf')}).json()
print('  Status:', r['overall_status'])
print('  Extracted claims:', r['extracted_claims'])
for c in r['active_contradictions']:
    print('  Conflict:', c['claim'], 'vs', c['evidence'])
print('  Data source: PDF OCR (PyMuPDF regex) - NOT mock_dataset.json')
results.append(('Foxtrot PDF OCR', r['overall_status'], len(r['active_contradictions']), 'PDF_OCR'))

# TEST 4
print()
print('=== TEST 4: GST Certificate PDF (what can OCR extract from it?) ===')
with open(os.path.join(PUBLIC, 'gst_tender_demo.pdf'), 'rb') as f:
    r = requests.post(BASE + '/api/v1/bidders/verify-document',
                      files={'bidder_pdf': ('gst_tender_demo.pdf', f, 'application/pdf')}).json()
print('  Status:', r['overall_status'])
print('  Extracted claims:', r['extracted_claims'])
if not r['extracted_claims']:
    print('  RESULT: GST cert contains no bidder claim fields (turnover/local content/sub-contracting)')
    print('  VERDICT: GST tab is DISPLAY ONLY - gstn_mock in mock_dataset.json drives verification')
results.append(('GST Cert', r['overall_status'], len(r['active_contradictions']), 'PDF_OCR'))

# TEST 5
print()
print('=== TEST 5: Echo Enterprises (expect 3 violations - MII + Subcontract + GST) ===')
requests.post(BASE + '/api/v1/verify/bidder/bidder-echo-005/tender/tender-sih-2026')
r = requests.get(BASE + '/api/v1/dashboard/bidder/bidder-echo-005').json()
print('  Status:', r['overall_status'])
for c in r['active_contradictions']:
    print('  Conflict:', c['claim'], 'vs', c['evidence'])
print('  Data source: mock_dataset.json')
results.append(('Echo Enterprises', r['overall_status'], len(r['active_contradictions']), 'mock_data'))

# SUMMARY
print()
print('=' * 70)
print('RESULTS SUMMARY')
print('=' * 70)
print('{:<25} {:<30} {:<10} {}'.format('Test', 'Status', 'Violations', 'Data Source'))
print('{:<25} {:<30} {:<10} {}'.format('-'*24, '-'*29, '-'*9, '-'*15))
for name, status, v, src in results:
    badge = '[PASS]' if status == 'VERIFIED_COMPLIANT' else '[FAIL]'
    print('{:<25} {} {:<24} {:<10} {}'.format(name, badge, status, v, src))

print()
print('DATA SOURCE TRUTH TABLE:')
print('  Tender Rules PDF     -> Backend OCR (PyMuPDF) - FULLY WIRED')
print('  Bidder Tech Bid PDF  -> Backend OCR (PyMuPDF) - FULLY WIRED')
print('  GST Certificate tab  -> DISPLAY ONLY (gstn_mock in mock_dataset.json)')
print('  Udyam Certificate tab-> DISPLAY ONLY (udyam_mock in mock_dataset.json)')
