import re
with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("match_status: 'PASS'", "result: 'PASS'")

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
