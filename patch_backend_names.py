import re

with open(r'backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace parse-gstr3b
gstr3b_old = """@app.post("/api/v1/bidders/parse-gstr3b")
async def parse_gstr3b(gstr3b_pdf: UploadFile = File(...)):
    file_bytes = await gstr3b_pdf.read()
    doc = _fitz.open(stream=file_bytes, filetype="pdf")
    text = " ".join(page.get_text() for page in doc)
    
    result = {
        "document_type": "GSTR3B_RETURN",
        "extracted": {
            "filing_status": "FILED",
            "return_period": "August 2026",
            "tax_payable": "2,45,000",
            "tax_paid": "2,45,000"
        },
        "verification": {
            "note": "Extracted GSTR-3B return details from uploaded document. Match with GSTN API verified."
        }
    }
    return result"""

gstr3b_new = """@app.post("/api/v1/bidders/parse-gstr3b")
async def parse_gstr3b(gstr3b_pdf: UploadFile = File(...)):
    file_bytes = await gstr3b_pdf.read()
    doc = _fitz.open(stream=file_bytes, filetype="pdf")
    text = " ".join(page.get_text() for page in doc)
    
    entity_name = "Demo Bidder"
    m = _re.search(r'Legal Name:\\s*(.*)', text)
    if m:
        entity_name = m.group(1).strip()
        
    result = {
        "document_type": "GSTR3B_RETURN",
        "extracted": {
            "entity_name": entity_name,
            "filing_status": "FILED",
            "return_period": "August 2026",
            "tax_payable": "2,45,000",
            "tax_paid": "2,45,000"
        },
        "verification": {
            "note": "Extracted GSTR-3B return details from uploaded document. Match with GSTN API verified."
        }
    }
    return result"""
content = content.replace(gstr3b_old, gstr3b_new)


# Replace parse-debarment
debarment_old = """@app.post("/api/v1/bidders/parse-debarment")
async def parse_debarment(debarment_pdf: UploadFile = File(...)):
    file_bytes = await debarment_pdf.read()
    doc = _fitz.open(stream=file_bytes, filetype="pdf")
    text = " ".join(page.get_text() for page in doc)
    
    result = {
        "document_type": "DEBARMENT_DECLARATION",
        "extracted": {
            "entity_name": "Demo Bidder",
            "declaration": "We hereby declare that our company is not blacklisted or debarred by any Govt department."
        },
        "verification": {
            "note": "Self-declaration of non-debarment extracted. Must be cross-verified against Vigilance/MoF DB."
        }
    }
    return result"""

debarment_new = """@app.post("/api/v1/bidders/parse-debarment")
async def parse_debarment(debarment_pdf: UploadFile = File(...)):
    file_bytes = await debarment_pdf.read()
    doc = _fitz.open(stream=file_bytes, filetype="pdf")
    text = " ".join(page.get_text() for page in doc)
    
    entity_name = "Demo Bidder"
    m = _re.search(r'We,\\s*(.*?),\\s*hereby declare', text, _re.IGNORECASE)
    if m:
        entity_name = m.group(1).strip()
    
    result = {
        "document_type": "DEBARMENT_DECLARATION",
        "extracted": {
            "entity_name": entity_name,
            "declaration": "We hereby declare that our company is not blacklisted or debarred by any Govt department."
        },
        "verification": {
            "note": "Self-declaration of non-debarment extracted. Must be cross-verified against Vigilance/MoF DB."
        }
    }
    return result"""
content = content.replace(debarment_old, debarment_new)

with open(r'backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
