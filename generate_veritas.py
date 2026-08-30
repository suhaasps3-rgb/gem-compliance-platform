import fitz  # PyMuPDF

def generate_veritas_pdf():
    doc = fitz.open()
    page = doc.new_page()
    
    text = """GOVERNMENT E-MARKETPLACE (GeM)
SIMULATED BID / REQUEST FOR PROPOSAL
AI COMPLIANCE VERIFICATION TEST DOCUMENT — VERITAS

1. Instructions to Bidders
1.4 A document submitted by a bidder shall not, by itself, override contradictory information obtained from an authoritative source.

2. Bidder Eligibility and Statutory Requirements
E-02 — Micro Enterprise: The bidder must be registered as a Micro Enterprise under the applicable MSME classification. The annual turnover of the bidder shall not exceed 10,00,00,000 (Rupees Ten Crore).

E-11 — OEM Authorisation: The bidder must submit a valid OEM authorisation letter identifying the bidder, OEM and product offered.
"""
    
    page.insert_text((50, 50), text, fontsize=10)
    
    # Save directly to Desktop
    desktop_path = r"C:\Users\Suhaas\OneDrive\Desktop\veritas_tender.pdf"
    doc.save(desktop_path)
    print(f"Created {desktop_path} successfully!")

if __name__ == "__main__":
    generate_veritas_pdf()
