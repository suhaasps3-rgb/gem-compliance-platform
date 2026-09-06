// src/components/PdfViewer/DocumentTabs.jsx
import React from 'react';
import { useDashboardStore } from '../../store/dashboardStore';

/**
 * Tabs to switch between Tender, GST, and Udyam PDFs.
 * Calls the backend /documents endpoint to fetch URLs (once on mount).
 */
export default function DocumentTabs() {
  const [urls, setUrls] = React.useState({});
  const selectedDocument = useDashboardStore((s) => s.selectedDocument);
  const setSelectedDocument = useDashboardStore((s) => s.setSelectedDocument);

  React.useEffect(() => {
    // fetch document URLs for a dummy tender id (could be dynamic)
    fetch('http://localhost:8000/api/v1/tenders/tender-demo-001/documents')
      .then((res) => res.json())
      .then(setUrls)
      .catch(() => setUrls({}));
  }, []);

  const mainTabs = [
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


  return (
    <div className="border-b border-gray-200 mb-2">
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
    </div>
  );
}
