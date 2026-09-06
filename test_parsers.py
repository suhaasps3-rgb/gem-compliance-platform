import sys, io, os, requests, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'http://localhost:8000'
PUBLIC = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance\frontend\public'

print("=" * 60)
print("TEST: GST Certificate Parser")
print("=" * 60)
with open(os.path.join(PUBLIC, 'gst_tender_demo.pdf'), 'rb') as f:
    r = requests.post(BASE + '/api/v1/bidders/parse-gst',
                      files={'gst_pdf': ('gst_tender_demo.pdf', f, 'application/pdf')}).json()

print("Document Type:", r['document_type'])
print("\nExtracted Fields:")
for k, v in r['extracted'].items():
    print(f"  {k}: {v}")
print("\nVerification Flags:")
for k, v in r['verification'].items():
    if k != 'note':
        print(f"  {k}: {v}")
print("  Note:", r['verification']['note'])

print()
print("=" * 60)
print("TEST: Udyam Certificate Parser")
print("=" * 60)
with open(os.path.join(PUBLIC, 'udyam_tender_demo.pdf'), 'rb') as f:
    r = requests.post(BASE + '/api/v1/bidders/parse-udyam',
                      files={'udyam_pdf': ('udyam_tender_demo.pdf', f, 'application/pdf')}).json()

print("Document Type:", r['document_type'])
print("\nExtracted Fields:")
for k, v in r['extracted'].items():
    print(f"  {k}: {v}")
print("\nVerification Flags:")
for k, v in r['verification'].items():
    if k != 'note':
        print(f"  {k}: {v}")
print("  Note:", r['verification']['note'])
