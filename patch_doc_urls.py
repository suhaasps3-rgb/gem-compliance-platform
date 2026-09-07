import re

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_doc_urls = r"""const DOC_URLS = {
  tender: '/tender_demo.pdf',
  gst:    '/gst_tender_demo.pdf',
  udyam:  '/udyam_tender_demo.pdf',
  epfo: '/epfo_demo.pdf',
  esic: '/esic_demo.pdf',
  startup: '/startup_india_demo.pdf',
  nsic: '/nsic_demo.pdf',
  work_order: '/work_order_1.pdf',
  turnover: '/ca_turnover.pdf',
  technical: '/technical_catalog.pdf'
};"""

new_doc_urls = """const DOC_URLS = {
  tender: '/tender_demo.pdf',
  gst:    '/gst_tender_demo.pdf',
  udyam:  '/udyam_tender_demo.pdf',
  epfo: '/epfo_demo.pdf',
  esic: '/esic_demo.pdf',
  startup: '/startup_india_demo.pdf',
  nsic: '/nsic_demo.pdf',
  work_order: '/work_order_1.pdf',
  turnover: '/ca_turnover.pdf',
  technical: '/technical_catalog.pdf',
  itr: '/tender_demo.pdf',
  mii: '/tender_demo.pdf',
  gstr3b: '/tender_demo.pdf',
  debarment: '/tender_demo.pdf'
};"""

content = content.replace(old_doc_urls, new_doc_urls)

with open(r'frontend\src\components\PdfViewer\Viewer.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
