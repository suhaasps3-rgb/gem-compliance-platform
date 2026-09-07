import re
with open(r'frontend\src\Dashboard.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "const clearVerifiedDocResult = useDashboardStore(s => s.clearVerifiedDocResult);",
    "const clearVerifiedDocResult = useDashboardStore(s => s.clearVerifiedDocResult);\n  const clearAllDocs = useDashboardStore(s => s.clearAllDocs);"
)

content = content.replace(
    "useEffect(() => {",
    "useEffect(() => {\n    clearAllDocs(); // Reset all uploaded docs when switching companies",
    1
)

with open(r'frontend\src\Dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
