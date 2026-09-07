import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add getUploadLabel function inside Viewer
label_func = """
  const getUploadLabel = () => {
    if (verifying) return 'Parsing...';
    const labels = {
      gst: 'Upload GST Certificate', udyam: 'Upload Udyam Certificate', epfo: 'Upload EPFO Statement', esic: 'Upload ESIC Challan',
      startup: 'Upload Startup Cert', nsic: 'Upload NSIC Cert', work_order: 'Upload Work Order', turnover: 'Upload CA Turnover',
      technical: 'Upload Tech Catalog', tender: 'Upload Bidder Document', itr: 'Upload ITR Return', mii: 'Upload MII Declaration',
      gstr3b: 'Upload GSTR-3B Return', debarment: 'Upload Debarment Decl.'
    };
    return labels[selectedDocument] || 'Upload Document';
  };
"""

# Insert right after the React state definitions
content = re.sub(r'const \[bhResult, setBhResult\]           = React\.useState\(null\);\n', 
                 r'const [bhResult, setBhResult]           = React.useState(null);\n' + label_func, content)

# Replace the hardcoded label logic in the UI
old_label_logic = r"\{verifying \? 'Parsing\.\.\.' :\s*selectedDocument === 'gst'\s*\? 'Upload GST Certificate' :\s*selectedDocument === 'udyam'\s*\? 'Upload Udyam Certificate' :\s*'Upload Bidder Document'\}"
content = re.sub(old_label_logic, "{getUploadLabel()}", content)

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
