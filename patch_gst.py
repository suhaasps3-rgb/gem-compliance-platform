import re

with open(r'backend\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """    # Mock GSTR Returns
    result["extracted"]["gstr_filing_status"] = "FILED"
    result["extracted"]["pending_returns"] = 0
    if "DEFAULTER" in text.upper() or "NON_FILER" in text.upper():
        result["extracted"]["gstr_filing_status"] = "PENDING"
        result["extracted"]["pending_returns"] = 3
    
    return result
"""

content = re.sub(r'    return result\n(?=.*?@app)', replacement, content, count=1, flags=re.DOTALL)

with open(r'backend\main.py', 'w', encoding='utf-8') as f:
    f.write(content)
