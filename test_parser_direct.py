import sys, json
sys.path.insert(0, 'backend')
from document_parsers import parse_turnover_ca

# Test the OLD ca_turnover.pdf in frontend/public
with open('frontend/public/ca_turnover.pdf', 'rb') as f:
    result = parse_turnover_ca(f.read())
print("=== OLD ca_turnover.pdf ===")
print(json.dumps(result, indent=2))

# Test the user's uploaded one from Signature_Testing
import os
sig_path = r'C:\Users\Suhaas\Downloads\GeM_Compliance_Test_Files\Signature_Testing\turnover_unsigned.pdf'
if os.path.exists(sig_path):
    with open(sig_path, 'rb') as f:
        result2 = parse_turnover_ca(f.read())
    print("\n=== turnover_unsigned.pdf ===")
    print(json.dumps(result2, indent=2))
