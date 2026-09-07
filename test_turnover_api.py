import requests

url = "http://localhost:8000/api/v1/bidders/parse-turnover"
files = {'turnover_pdf': open(r'C:\Users\Suhaas\Downloads\GeM_Compliance_Test_Files\Signature_Testing\turnover_unsigned.pdf', 'rb')}
r = requests.post(url, files=files)
print(r.json())
