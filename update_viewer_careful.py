with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to UPLOAD_CONFIG
if "gstr3b: {" not in content:
    content = content.replace(
        "turnover: { endpoint: '/api/v1/bidders/parse-turnover', field: 'turnover_pdf' }",
        "turnover: { endpoint: '/api/v1/bidders/parse-turnover', field: 'turnover_pdf' },\n  gstr3b: { endpoint: '/api/v1/bidders/parse-gstr3b', field: 'gstr3b_pdf' },\n  debarment: { endpoint: '/api/v1/bidders/parse-debarment', field: 'debarment_pdf' }"
    )

# Add to handleFileUpload if block
if "setGstr3bParseResult" not in content:
    content = content.replace(
        "else if (selectedDocument === 'nsic') setNsicParseResult(data);",
        "else if (selectedDocument === 'nsic') setNsicParseResult(data);\n        else if (selectedDocument === 'gstr3b') useDashboardStore.getState().setGstr3bParseResult(data);\n        else if (selectedDocument === 'debarment') useDashboardStore.getState().setDebarmentParseResult(data);"
    )

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
