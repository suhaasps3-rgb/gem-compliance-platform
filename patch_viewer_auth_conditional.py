import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

target = """// Also fire off authenticity check in parallel
        const authFormData = new FormData();
        authFormData.append('file', file);
        fetch('http://localhost:8000/api/v1/verify-authenticity', { method: 'POST', body: authFormData })
          .then(r => r.json())
          .then(data => {
              useDashboardStore.getState().setVisualAuthResult(data);
          })
          .catch(err => console.error(err));"""

replacement = """// Only check physical signature/stamp for documents that legally require them
        const requiresSignature = ['turnover', 'work_order', 'technical', 'mii', 'debarment', 'tender'].includes(selectedDocument);
        if (requiresSignature) {
          const authFormData = new FormData();
          authFormData.append('file', file);
          fetch('http://localhost:8000/api/v1/verify-authenticity', { method: 'POST', body: authFormData })
            .then(r => r.json())
            .then(data => {
                useDashboardStore.getState().setVisualAuthResult({ ...data, document_type: selectedDocument });
            })
            .catch(err => console.error(err));
        } else {
          useDashboardStore.getState().setVisualAuthResult(null);
        }"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("WARNING: target not found in Viewer.jsx")

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
