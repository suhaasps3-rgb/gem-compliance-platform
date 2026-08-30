from rule_compiler import TenderRuleCompiler

def test_tender_compiler():
    compiler = TenderRuleCompiler()
    
    # Simulate a fake PDF byte stream
    fake_pdf_bytes = b"%PDF-1.4\n%Fake Tender Document..."
    
    results = compiler.extract_rules_from_pdf(fake_pdf_bytes, "tender_document.pdf")
    
    assert len(results) == 3, "Expected 3 simulated rules extracted"
    
    msme_rule = results[0]
    assert "Turnover <= \u20b910Cr" in msme_rule["description"]
    assert "mapped_regulatory_id" in msme_rule
    
    gfr_rule = results[2]
    assert "GFR 2017 Rule 175" in gfr_rule["clause"]

    print("PASS: LLM Tender-to-Rule Compiler tests passed. Rules extracted cleanly.")

if __name__ == "__main__":
    test_tender_compiler()
