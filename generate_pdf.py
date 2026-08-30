import fitz  # PyMuPDF

def generate_mock_pdf():
    # Create a new empty PDF document
    doc = fitz.open()
    
    # Add a new page
    page = doc.new_page()
    
    # Define the text we want in our fake tender
    text = """GOVERNMENT OF INDIA
MINISTRY OF COMMERCE AND INDUSTRY
GOVERNMENT e MARKETPLACE (GeM)

TENDER NOTIFICATION: SIH-2026-XYZ

Section 1: Introduction
This is a Request for Proposal for the supply of customized software solutions.

Section 2: Eligibility Criteria
4(A) MSME Status: Bidder must be registered as a Micro Enterprise (Turnover <= INR 10 Cr).
4(B) EMD Exemption: Startups and MSMEs are exempted from Earnest Money Deposit.

Section 3: Code of Integrity
Any omission or misrepresentation that may mislead to obtain financial benefit is strictly prohibited under GFR 2017 Rule 175.
"""
    
    # Insert text into the page (coordinates x, y)
    page.insert_text((50, 50), text, fontsize=12)
    
    # Save the PDF to the workspace
    doc.save("mock_tender_document.pdf")
    print("Created mock_tender_document.pdf successfully!")

if __name__ == "__main__":
    generate_mock_pdf()
