import os

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance'

# 1. Update dashboardStore.js
f = os.path.join(ROOT, 'frontend', 'src', 'store', 'dashboardStore.js')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

new_store_methods = """
  gstParseResult: null,
  setGstParseResult: (res) => set({ gstParseResult: res }),
  clearGstParseResult: () => set({ gstParseResult: null }),

  udyamParseResult: null,
  setUdyamParseResult: (res) => set({ udyamParseResult: res }),
  clearUdyamParseResult: () => set({ udyamParseResult: null }),

  epfoParseResult: null,
  setEpfoParseResult: (res) => set({ epfoParseResult: res }),
  clearEpfoParseResult: () => set({ epfoParseResult: null }),

  esicParseResult: null,
  setEsicParseResult: (res) => set({ esicParseResult: res }),
  clearEsicParseResult: () => set({ esicParseResult: null }),

  startupParseResult: null,
  setStartupParseResult: (res) => set({ startupParseResult: res }),
  clearStartupParseResult: () => set({ startupParseResult: null }),

  nsicParseResult: null,
  setNsicParseResult: (res) => set({ nsicParseResult: res }),
  clearNsicParseResult: () => set({ nsicParseResult: null }),
"""
# Replace the chunk
import re
content = re.sub(
    r'gstParseResult: null,.*?nsicParseResult: \(res\) => set\(\{ nsicParseResult: res \}\),',
    new_store_methods.strip() + ',',
    content,
    flags=re.DOTALL
)

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)
print('dashboardStore.js patched')

# 2. Update GovDocPanel.jsx
f = os.path.join(ROOT, 'frontend', 'src', 'GovDocPanel.jsx')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

import_lines = """
  const gstResult   = useDashboardStore(s => s.gstParseResult);
  const udyamResult = useDashboardStore(s => s.udyamParseResult);
  const epfoResult  = useDashboardStore(s => s.epfoParseResult);
  const esicResult  = useDashboardStore(s => s.esicParseResult);
  const startupResult = useDashboardStore(s => s.startupParseResult);
  const nsicResult  = useDashboardStore(s => s.nsicParseResult);
  
  const clearGst    = useDashboardStore(s => s.clearGstParseResult);
  const clearUdyam  = useDashboardStore(s => s.clearUdyamParseResult);
  const clearEpfo   = useDashboardStore(s => s.clearEpfoParseResult);
  const clearEsic   = useDashboardStore(s => s.clearEsicParseResult);
  const clearStartup = useDashboardStore(s => s.clearStartupParseResult);
  const clearNsic   = useDashboardStore(s => s.clearNsicParseResult);

  if (!gstResult && !udyamResult && !epfoResult && !esicResult && !startupResult && !nsicResult) return null;
"""
content = re.sub(
    r'  const gstResult.*?if \(!gstResult && !udyamResult\) return null;',
    import_lines.strip(),
    content,
    flags=re.DOTALL
)

new_panels = """
      {/* ── EPFO Panel ── */}
      {epfoResult && (
        <Panel title="EPFO Statement (ECR)" color="blue" icon="🏦" onClear={clearEpfo}>
          <Field label="Employer Name" value={epfoResult.extracted?.employer_name} status="ok" />
          <Field label="Employer Code" value={epfoResult.extracted?.employer_code} status={epfoResult.verification?.employer_code_found ? 'ok' : 'fail'} />
          <Field label="Contribution Period" value={epfoResult.extracted?.contribution_period} />
          <Field label="Employee Count" value={epfoResult.extracted?.employee_count} />
          <Field label="Total Amount" value={`₹ ${epfoResult.extracted?.total_contribution || '0'}`} />
          <Field label="Status" value={epfoResult.verification?.contribution_status} status={epfoResult.verification?.contribution_verified ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── ESIC Panel ── */}
      {esicResult && (
        <Panel title="ESIC Challan" color="green" icon="🏥" onClear={clearEsic}>
          <Field label="Employer Name" value={esicResult.extracted?.employer_name} status="ok" />
          <Field label="Employer Code" value={esicResult.extracted?.employer_code} status={esicResult.verification?.employer_code_found ? 'ok' : 'fail'} />
          <Field label="Contribution Period" value={esicResult.extracted?.contribution_period} />
          <Field label="Total Amount" value={`₹ ${esicResult.extracted?.contribution_amount || '0'}`} />
          <Field label="Status" value={esicResult.verification?.contribution_status} status={esicResult.verification?.esic_verified ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── Startup India Panel ── */}
      {startupResult && (
        <Panel title="Startup India Certificate" color="blue" icon="🚀" onClear={clearStartup}>
          <Field label="Entity Name" value={startupResult.extracted?.entity_name} status="ok" />
          <Field label="Recognition No" value={startupResult.extracted?.recognition_number} status={startupResult.verification?.recognition_number_found ? 'ok' : 'fail'} />
          <Field label="Recognition Date" value={startupResult.extracted?.recognition_date} />
          <Field label="Valid Till" value={startupResult.extracted?.validity} />
          <Field label="Certificate Status" value={startupResult.extracted?.certificate_status} status={startupResult.verification?.certificate_active ? 'ok' : 'fail'} />
          <Field label="EMD Exemption" value={startupResult.verification?.emd_exemption_supported ? 'ELIGIBLE' : 'NOT ELIGIBLE'} status={startupResult.verification?.emd_exemption_supported ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── NSIC Panel ── */}
      {nsicResult && (
        <Panel title="NSIC Certificate" color="green" icon="🏭" onClear={clearNsic}>
          <Field label="Enterprise Name" value={nsicResult.extracted?.enterprise_name} status="ok" />
          <Field label="Certificate No" value={nsicResult.extracted?.certificate_number} status={nsicResult.verification?.certificate_number_found ? 'ok' : 'fail'} />
          <Field label="Category" value={nsicResult.extracted?.category} />
          <Field label="Date of Issue" value={nsicResult.extracted?.issue_date} />
          <Field label="Valid Till" value={nsicResult.extracted?.validity} />
          <Field label="EMD Exemption" value={nsicResult.verification?.emd_exemption_supported ? 'ELIGIBLE' : 'NOT ELIGIBLE'} status={nsicResult.verification?.emd_exemption_supported ? 'ok' : 'warn'} />
        </Panel>
      )}
    </div>
"""
content = content.replace("    </div>\n  );\n}", new_panels + "  );\n}")

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)
print('GovDocPanel.jsx patched')

# 3. Update Viewer.jsx
f = os.path.join(ROOT, 'frontend', 'src', 'components', 'PdfViewer', 'Viewer.jsx')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

button_label_code = """
  const getUploadLabel = () => {
    if (verifying) return 'Parsing...';
    const labels = {
      gst: 'Upload GST Certificate',
      udyam: 'Upload Udyam Certificate',
      epfo: 'Upload EPFO Statement',
      esic: 'Upload ESIC Challan',
      startup: 'Upload Startup Cert',
      nsic: 'Upload NSIC Cert',
      work_order: 'Upload Work Order',
      turnover: 'Upload CA Turnover',
      technical: 'Upload Tech Catalog',
      tender: 'Upload Bidder Document'
    };
    return labels[selectedDocument] || 'Upload Document';
  };

  const getSuccessBadge = () => {
    const labels = {
      gst: 'GST Parsed',
      udyam: 'Udyam Parsed',
      epfo: 'EPFO Parsed',
      esic: 'ESIC Parsed',
      startup: 'Startup Parsed',
      nsic: 'NSIC Parsed',
      work_order: 'Work Order Parsed',
      turnover: 'Turnover Parsed',
      technical: 'Catalog Parsed',
      tender: 'Verified'
    };
    return `✓ ${labels[selectedDocument] || 'Parsed'}`;
  };
"""

if 'const getUploadLabel' not in content:
    content = content.replace(
        "const pdfUrl = customPdfUrl || DOC_URLS[selectedDocument] || DOC_URLS.tender;",
        "const pdfUrl = customPdfUrl || DOC_URLS[selectedDocument] || DOC_URLS.tender;\n" + button_label_code
    )

    # replace button logic
    old_btn_logic = """          {verifying ? 'Parsing...' :
           selectedDocument === 'gst'   ? 'Upload GST Certificate' :
           selectedDocument === 'udyam' ? 'Upload Udyam Certificate' :
           'Upload Bidder Document'}"""
    content = content.replace(old_btn_logic, "          {getUploadLabel()}")

    # replace success badge
    old_success_badge = "✓ {selectedDocument === 'gst' ? 'GST Parsed' : selectedDocument === 'udyam' ? 'Udyam Parsed' : 'Verified'}"
    content = content.replace(old_success_badge, "{getSuccessBadge()}")

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print('Viewer.jsx patched')
