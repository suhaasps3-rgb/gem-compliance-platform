with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update UPLOAD_CONFIG
old_config = "debarment: { endpoint: '/api/v1/bidders/parse-debarment', field: 'debarment_pdf' }\n};"
new_config = """debarment: { endpoint: '/api/v1/bidders/parse-debarment', field: 'debarment_pdf' }\n};\n"""
# Wait, actually, the original doesn't have debarment! I need to see what's currently in `Viewer.jsx`.
