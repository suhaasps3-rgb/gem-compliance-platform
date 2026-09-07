import requests

url = "http://localhost:8000/api/v1/bidders/parse-work-order"
files = {'wo_pdf': open(r'C:\Users\Suhaas\Downloads\GeM_Compliance_Test_Files\Signature_Testing\work_order_unsigned.pdf', 'rb')}
r = requests.post(url, files=files)
print(r.json())
