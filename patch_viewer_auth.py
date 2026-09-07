import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

target = "const res = await fetch(`http://localhost:8000${cfg.endpoint}`, { method: 'POST', body: formData });"
replacement = """const res = await fetch(`http://localhost:8000${cfg.endpoint}`, { method: 'POST', body: formData });
        
        // Also fire off authenticity check in parallel
        const authFormData = new FormData();
        authFormData.append('file', file);
        fetch('http://localhost:8000/api/v1/verify-authenticity', { method: 'POST', body: authFormData })
          .then(r => r.json())
          .then(data => {
              useDashboardStore.getState().setVisualAuthResult(data);
          })
          .catch(err => console.error(err));"""

if "verify-authenticity" not in content:
    content = content.replace(target, replacement)
    
    with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
        f.write(content)
