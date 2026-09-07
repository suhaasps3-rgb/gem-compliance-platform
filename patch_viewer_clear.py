import re
with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "setLoadError(false); setVerifyStatus(null); setVerifying(true);",
    "setLoadError(false); setVerifyStatus(null); setVerifying(true); useDashboardStore.getState().setVisualAuthResult(null);"
)
content = content.replace(
    "setBhResult(null); setShowBhashini(false); }}",
    "setBhResult(null); setShowBhashini(false); useDashboardStore.getState().setVisualAuthResult(null); }}"
)

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
