import re

with open(r'backend\document_parsers.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    r"[A-Z][A-Za-z\s&\.]+(?:Ltd|Limited|Corporation|Corp|Industries|ONGC|HPCL|BPCL|CPCL|Reliance|Tata)",
    r"[A-Z][A-Za-z \t&\.]+(?:Ltd|Limited|Corporation|Corp|Industries|ONGC|HPCL|BPCL|CPCL|Reliance|Tata)"
)

content = content.replace(
    r"[A-Z][A-Za-z\s&\.]+(?:Ltd|Limited|Pvt|Private|LLP|Services)?",
    r"[A-Z][A-Za-z \t&\.]+(?:Ltd|Limited|Pvt|Private|LLP|Services)?"
)

with open(r'backend\document_parsers.py', 'w', encoding='utf-8') as f:
    f.write(content)
