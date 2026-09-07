import asyncio
from batch_engine import create_batch, process_batch_background, get_batch_state
with open('../batch_demo.zip', 'rb') as f:
    zip_b = f.read()
bid = create_batch(zip_b)
process_batch_background(bid, zip_b)
state = get_batch_state(bid)
import json
for k, v in state['bidders'].items():
    print(f"{k}: {v['compliance_score']} - {v.get('experience_result', {}).get('eligible_cr') if v.get('experience_result') else 0} Cr - {v['risk_level']}")
