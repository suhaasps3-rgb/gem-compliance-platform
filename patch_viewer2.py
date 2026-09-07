import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("else if (selectedDocument === 'mii') setMiiParseResult(data);", 
"""else if (selectedDocument === 'mii') setMiiParseResult(data);
        else if (selectedDocument === 'gstr3b') useDashboardStore.getState().setGstr3bParseResult(data);
        else if (selectedDocument === 'debarment') useDashboardStore.getState().setDebarmentParseResult(data);""")

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
