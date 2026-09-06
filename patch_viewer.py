import os

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance'

# 1. Update DocumentTabs.jsx
f = os.path.join(ROOT, 'frontend', 'src', 'components', 'PdfViewer', 'DocumentTabs.jsx')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

new_tabs = """  const mainTabs = [
    { id: 'tender', label: 'Tender Document' },
    { id: 'gst', label: 'GST Certificate' },
    { id: 'udyam', label: 'Udyam Certificate' },
  ];
  
  const [showAdditional, setShowAdditional] = React.useState(false);
  const additionalTabs = [
    { id: 'epfo', label: 'EPFO Statement' },
    { id: 'esic', label: 'ESIC Challan' },
    { id: 'startup', label: 'Startup India' },
    { id: 'nsic', label: 'NSIC Certificate' },
    { id: 'work_order', label: 'Work Order' },
    { id: 'turnover', label: 'CA Turnover' },
    { id: 'technical', label: 'Tech Catalog' }
  ];
"""

if 'const mainTabs =' not in content:
    content = content.replace(
        "  const tabs = [\n    { id: 'tender', label: 'Tender Document' },\n    { id: 'gst', label: 'GST Certificate' },\n    { id: 'udyam', label: 'Udyam Certificate' },\n  ];",
        new_tabs
    )
    
    new_nav = """    <div className="border-b border-gray-200 mb-2">
      <nav className="flex flex-wrap space-x-2">
        {mainTabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSelectedDocument(tab.id)}
            className={`px-3 py-2 text-sm font-medium focus:outline-none ${selectedDocument === tab.id ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600 hover:text-gray-900'}`}
          >
            {tab.label}
          </button>
        ))}
        <div className="relative">
          <button 
            onClick={() => setShowAdditional(!showAdditional)}
            className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 focus:outline-none flex items-center gap-1"
          >
            Additional Docs ▼
          </button>
          {showAdditional && (
            <div className="absolute top-full left-0 mt-1 bg-white border rounded shadow-lg z-10 w-48 py-1">
              {additionalTabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => { setSelectedDocument(tab.id); setShowAdditional(false); }}
                  className={`block w-full text-left px-4 py-2 text-sm hover:bg-gray-50 ${selectedDocument === tab.id ? 'text-blue-600 font-bold bg-blue-50' : 'text-gray-700'}`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </nav>
    </div>"""
    
    old_nav = """    <div className="border-b border-gray-200 mb-2">
      <nav className="flex space-x-4">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSelectedDocument(tab.id)}
            className={`px-4 py-2 text-sm font-medium focus:outline-none ${selectedDocument === tab.id ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'}`}
          >
            {tab.label}
          </button>
        ))}
      </nav>
    </div>"""
    content = content.replace(old_nav, new_nav)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print("DocumentTabs.jsx updated.")

# 2. Update Viewer.jsx
f = os.path.join(ROOT, 'frontend', 'src', 'components', 'PdfViewer', 'Viewer.jsx')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

if 'epfo:' not in content:
    content = content.replace(
        "  udyam:  '/udyam_tender_demo.pdf',\n};",
        "  udyam:  '/udyam_tender_demo.pdf',\n  epfo: '/epfo_demo.pdf',\n  esic: '/esic_demo.pdf',\n  startup: '/startup_india_demo.pdf',\n  nsic: '/nsic_demo.pdf',\n  work_order: '/work_order_1.pdf',\n  turnover: '/ca_turnover.pdf',\n  technical: '/technical_catalog.pdf'\n};"
    )

    content = content.replace(
        "  udyam:  { endpoint: '/api/v1/bidders/parse-udyam',      field: 'udyam_pdf' },\n};",
        "  udyam:  { endpoint: '/api/v1/bidders/parse-udyam',      field: 'udyam_pdf' },\n  epfo: { endpoint: '/api/v1/bidders/parse-epfo', field: 'epfo_pdf' },\n  esic: { endpoint: '/api/v1/bidders/parse-esic', field: 'esic_pdf' },\n  startup: { endpoint: '/api/v1/bidders/parse-startup', field: 'startup_pdf' },\n  nsic: { endpoint: '/api/v1/bidders/parse-nsic', field: 'nsic_pdf' },\n  work_order: { endpoint: '/api/v1/bidders/parse-work-order', field: 'wo_pdf' },\n  turnover: { endpoint: '/api/v1/bidders/parse-turnover', field: 'turnover_pdf' }\n};"
    )

    content = content.replace(
        "const setUdyamParseResult = useDashboardStore((s) => s.setUdyamParseResult);",
        "const setUdyamParseResult = useDashboardStore((s) => s.setUdyamParseResult);\n  const setEpfoParseResult = useDashboardStore((s) => s.setEpfoParseResult);\n  const setEsicParseResult = useDashboardStore((s) => s.setEsicParseResult);\n  const setStartupParseResult = useDashboardStore((s) => s.setStartupParseResult);\n  const setNsicParseResult = useDashboardStore((s) => s.setNsicParseResult);"
    )

    content = content.replace(
        "else if (selectedDocument === 'udyam') setUdyamParseResult(data);",
        "else if (selectedDocument === 'udyam') setUdyamParseResult(data);\n      else if (selectedDocument === 'epfo') setEpfoParseResult(data);\n      else if (selectedDocument === 'esic') setEsicParseResult(data);\n      else if (selectedDocument === 'startup') setStartupParseResult(data);\n      else if (selectedDocument === 'nsic') setNsicParseResult(data);"
    )
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print("Viewer.jsx updated.")
