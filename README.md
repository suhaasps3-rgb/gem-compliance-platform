# GeM Compliance Platform

An intelligent, deterministic compliance engine for government procurement, built for the Smart India Hackathon.

## The ""
This platform does not use AI to disqualify bidders. Instead, it uses a **NetworkX Evidence Provenance Graph** to deterministically cross-reference PDF claims against authoritative government APIs (MCA21, Udyam, GSTN). 

When a contradiction is found (e.g., a bidder claims Micro MSME status, but MCA21 reports turnover exceeding the limit), the platform surfaces it in a split-screen UI and empowers the Procurement Officer to instantly generate a legally-formatted Show-Cause Notice citing the exact **GFR 2017** regulations. All officer actions are securely logged to a **SHA-256 Tamper-Evident Ledger** that aggressively masks PII to comply with the DPDP Act.

## Architecture
- **Backend:** Python, FastAPI, NetworkX (Graph Traversal)
- **Frontend:** React, Vite, Tailwind CSS
- **Data Engine:** Deterministic rule resolution backed by simulated LLM extraction.

## Running Locally

### 1. Start the Backend
```bash
cd backend
python -m venv venv
# Activate venv (Windows: .\venv\Scripts\Activate.ps1 | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python main.py
```

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` to view the Dashboard. Toggle between "Acme Corp" (Green/Compliant) and "Delta Solutions" (Red/Contradiction) to see the engine in action.

## Testing
Run the backend automated tests:
```bash
cd backend
# With venv activated
python test_graph.py
python test_collusion.py
python test_compiler.py
```
