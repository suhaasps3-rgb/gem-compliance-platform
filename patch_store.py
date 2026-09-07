import re
with open(r'frontend\src\store\dashboardStore.js', 'r', encoding='utf-8') as f:
    content = f.read()

clear_all = """
  clearAllDocs: () => set({
    verifiedDocResult: null,
    gstParseResult: null,
    udyamParseResult: null,
    epfoParseResult: null,
    esicParseResult: null,
    startupParseResult: null,
    nsicParseResult: null,
    turnoverParseResult: null,
    itrParseResult: null,
    miiParseResult: null,
    gstr3bParseResult: null,
    debarmentParseResult: null,
    technicalMatrixResult: null,
    experienceResult: null,
    visualAuthResult: null,
  }),
"""

if "clearAllDocs" not in content:
    content = content.replace("clearDebarmentParseResult: () => set({ debarmentParseResult: null }),", "clearDebarmentParseResult: () => set({ debarmentParseResult: null }),\n" + clear_all)
    with open(r'frontend\src\store\dashboardStore.js', 'w', encoding='utf-8') as f:
        f.write(content)
