import requests, json

# Test the old ca_turnover.pdf that the user is uploading from the frontend
url = "http://localhost:8000/api/v1/bidders/parse-turnover"
files = {'turnover_pdf': open('frontend/public/ca_turnover.pdf', 'rb')}
r = requests.post(url, files=files)
print(json.dumps(r.json(), indent=2))
