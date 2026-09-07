import requests
import json
import time

url = 'http://localhost:8000/api/v1/batch/upload'
zip_path = r'C:\Users\Suhaas\Downloads\GeM_Compliance_Test_Files\batch_demo_3_bidders.zip'
with open(zip_path, 'rb') as f:
    r = requests.post(url, files={'batch_zip': f})

print('Upload response:', r.json())
batch_id = r.json().get('batch_id')

if batch_id:
    for i in range(12):
        time.sleep(1)
        st = requests.get(f'http://localhost:8000/api/v1/batch/{batch_id}').json()
        status = st.get('status')
        print(f'Poll {i+1}: status={status}')
        if status == 'COMPLETED':
            print('\n=== BATCH PROCESSING RESULTS ===')
            for b_id, b_info in st.get('bidders', {}).items():
                print(f"Bidder: {b_info.get('name')} ({b_id})")
                print(f"  Score: {b_info.get('compliance_score')}")
                print(f"  Risk: {b_info.get('risk_level')}")
                print(f"  Documents Processed: {b_info.get('doc_count')}")
            break
