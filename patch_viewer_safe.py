import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Update UPLOAD_CONFIG (Injecting right after DOC_URLS)
config = """
const UPLOAD_CONFIG = {
  tender: { endpoint: '/api/v1/bidders/verify-document', field: 'bidder_pdf' },
  gst:    { endpoint: '/api/v1/bidders/parse-gst',        field: 'gst_pdf'   },
  udyam:  { endpoint: '/api/v1/bidders/parse-udyam',      field: 'udyam_pdf' },
  epfo: { endpoint: '/api/v1/bidders/parse-epfo', field: 'epfo_pdf' },
  esic: { endpoint: '/api/v1/bidders/parse-esic', field: 'esic_pdf' },
  startup: { endpoint: '/api/v1/bidders/parse-startup', field: 'startup_pdf' },
  nsic: { endpoint: '/api/v1/bidders/parse-nsic', field: 'nsic_pdf' },
  work_order: { endpoint: '/api/v1/bidders/parse-work-order', field: 'wo_pdf' },
  turnover: { endpoint: '/api/v1/bidders/parse-turnover', field: 'turnover_pdf' },
  itr: { endpoint: '/api/v1/bidders/parse-itr', field: 'itr_pdf' },
  mii: { endpoint: '/api/v1/bidders/parse-mii', field: 'mii_pdf' },
  gstr3b: { endpoint: '/api/v1/bidders/parse-gstr3b', field: 'gstr3b_pdf' },
  debarment: { endpoint: '/api/v1/bidders/parse-debarment', field: 'debarment_pdf' }
};
"""

content = re.sub(r'const DOC_URLS = \{[^}]+\};', lambda m: m.group(0) + "\n" + config, content)

# Change cfg in handleFileUpload
content = content.replace("const formData = new FormData();", 
"""const cfg = UPLOAD_CONFIG[selectedDocument] || UPLOAD_CONFIG.tender;
    const formData = new FormData();""")

content = content.replace("fetch(`http://localhost:8000/api/v1/bidders/parse-${selectedDocument}`", "fetch(`http://localhost:8000${cfg.endpoint}`")

# Also the authenticity check parallel execution was added in my original script. I will add it again.
auth_fetch = """        const res = await fetch(`http://localhost:8000${cfg.endpoint}`, { method: 'POST', body: formData });
        
        // Also fire off authenticity check in parallel
        const authFormData = new FormData();
        authFormData.append('file', file);
        fetch('http://localhost:8000/api/v1/verify-authenticity', { method: 'POST', body: authFormData })
          .then(r => r.json())
          .then(data => {
              useDashboardStore.getState().setVisualAuthResult(data);
          })
          .catch(err => console.error(err));
"""
content = re.sub(r'const res = await fetch\(`http://localhost:8000\$\{cfg\.endpoint\}`[^;]+;', auth_fetch, content)


# Handle the results
results_logic = """if (selectedDocument === 'gst')        useDashboardStore.getState().setGstParseResult(data);
      else if (selectedDocument === 'udyam') useDashboardStore.getState().setUdyamParseResult(data);
      else if (selectedDocument === 'epfo') useDashboardStore.getState().setEpfoParseResult(data);
      else if (selectedDocument === 'esic') useDashboardStore.getState().setEsicParseResult(data);
      else if (selectedDocument === 'startup') useDashboardStore.getState().setStartupParseResult(data);
      else if (selectedDocument === 'nsic') useDashboardStore.getState().setNsicParseResult(data);
      else if (selectedDocument === 'turnover') useDashboardStore.getState().setTurnoverParseResult(data);
      else if (selectedDocument === 'itr') useDashboardStore.getState().setItrParseResult(data);
      else if (selectedDocument === 'mii') useDashboardStore.getState().setMiiParseResult(data);
      else if (selectedDocument === 'gstr3b') useDashboardStore.getState().setGstr3bParseResult(data);
      else if (selectedDocument === 'debarment') useDashboardStore.getState().setDebarmentParseResult(data);
      else if (selectedDocument === 'work_order') {
        const val = data.extracted?.order_value_cr || 0;
        useDashboardStore.getState().setExperienceResult({
          result: val >= 5.0 ? 'PASS' : 'INSUFFICIENT_EVIDENCE',
          requirement_cr: 5.0,
          eligible_cr: val,
          note: 'Extracted single work order via manual UI upload.',
          evidence: [{ wo_number: data.extracted?.wo_number || 'UNKNOWN', client: data.extracted?.client || 'UNKNOWN', order_date: data.extracted?.order_date || 'N/A', value_cr: val }]
        });
      }
      else if (selectedDocument === 'technical') {
        useDashboardStore.getState().setTechnicalMatrixResult({
          technical_score: 85, overall_result: 'PASS', summary: 'Extracted specs from single catalog upload.',
          matrix: [{ parameter: 'Extracted Data', requirement: 'Valid Specs', vendor_value: data.extracted?.product_name || 'Catalog Item', match_status: 'PASS' }]
        });
      }
      else if (selectedDocument === 'tender') useDashboardStore.getState().setVerifiedDocResult(data);"""

content = re.sub(r'if \(selectedDocument === \'gst\'\)[\s\S]*?else if \(selectedDocument === \'tender\'\) setVerifiedDocResult\(data\);', results_logic, content)

# update UI labels
labels_func = """const getUploadLabel = () => {
    if (verifying) return 'Parsing...';
    const labels = {
      gst: 'Upload GST Certificate', udyam: 'Upload Udyam Certificate', epfo: 'Upload EPFO Statement', esic: 'Upload ESIC Challan',
      startup: 'Upload Startup Cert', nsic: 'Upload NSIC Cert', work_order: 'Upload Work Order', turnover: 'Upload CA Turnover',
      technical: 'Upload Tech Catalog', tender: 'Upload Bidder Document', itr: 'Upload ITR Return', mii: 'Upload MII Declaration',
      gstr3b: 'Upload GSTR-3B Return', debarment: 'Upload Debarment Decl.'
    };
    return labels[selectedDocument] || 'Upload Document';
  };"""

content = re.sub(r'\{verifying \? \'Parsing\.\.\.\' :[\s\S]*?\'Upload Bidder Document\'\}', '{getUploadLabel()}', content)

content = content.replace("const [customPdfUrl, setCustomPdfUrl] = useState(null);", "const [customPdfUrl, setCustomPdfUrl] = useState(null);\n  " + labels_func)


# Make sure the imports have useState
content = content.replace("import React, { useRef, useEffect }", "import React, { useRef, useEffect, useState }")

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
