import requests

url = "http://localhost:8000/api/v1/bidders/parse-debarment"
files = {'debarment_pdf': open('backend/static/debarment_demo.pdf', 'rb')}
r = requests.post(url, files=files)
print(r.json())
