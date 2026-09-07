import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Update UPLOAD_CONFIG
config_replacement = """  const UPLOAD_CONFIG = {
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
};"""

content = re.sub(r'  const UPLOAD_CONFIG = \{.*?\n  \};', config_replacement, content, flags=re.DOTALL)

# Update getUploadLabel
label_replacement = """    const labels = {
      gst: 'Upload GST Certificate',
      udyam: 'Upload Udyam Certificate',
      epfo: 'Upload EPFO Statement',
      esic: 'Upload ESIC Challan',
      startup: 'Upload Startup Cert',
      nsic: 'Upload NSIC Cert',
      work_order: 'Upload Work Order',
      turnover: 'Upload CA Turnover',
      technical: 'Upload Tech Catalog',
      tender: 'Upload Bidder Document',
      itr: 'Upload ITR Return',
      mii: 'Upload MII Declaration',
      gstr3b: 'Upload GSTR-3B Return',
      debarment: 'Upload Debarment Decl.'
    };"""

content = re.sub(r'    const labels = \{.*?    \};', label_replacement, content, flags=re.DOTALL)

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
