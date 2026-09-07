import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("gstr3b: '/tender_demo.pdf'", "gstr3b: '/gstr3b_demo.pdf'")
content = content.replace("debarment: '/tender_demo.pdf'", "debarment: '/debarment_demo.pdf'")

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
