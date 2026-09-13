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
    fetch(`${import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')}/api/v1/tenders/tender-demo-001/documents`)
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
    { id: 'technical', label: 'Tech Catalog' },
    { id: 'itr', label: 'ITR Return' },
    { id: 'mii', label: 'MII Declaration' },
    { id: 'gstr3b', label: 'GSTR-3B Return' },
    { id: 'debarment', label: 'Debarment Decl.' }
  ];


  const activeAdditional = additionalTabs.find(t => t.id === selectedDocument);

  return (
    <div className="border-b border-slate-200 mb-2 pb-1 shrink-0">
      <nav className="flex flex-wrap items-center gap-1.5">
        {mainTabs.map((tab) => {
          const isActive = selectedDocument === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setSelectedDocument(tab.id)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                isActive
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 bg-white border border-slate-200'
              }`}
            >
              {tab.label}
            </button>
          );
        })}

        <div className="relative">
          <button 
            onClick={() => setShowAdditional(!showAdditional)}
            className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all flex items-center gap-1.5 border ${
              activeAdditional
                ? 'bg-blue-50 text-blue-700 border-blue-300 shadow-xs'
                : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100 hover:text-slate-900'
            }`}
          >
            <span>{activeAdditional ? `Doc: ${activeAdditional.label}` : 'More Statutory Docs'}</span>
            <svg className={`w-3 h-3 transition-transform ${showAdditional ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {showAdditional && (
            <div className="absolute top-full left-0 mt-1 bg-white border border-slate-200 rounded-lg shadow-xl z-50 w-52 py-1 max-h-72 overflow-y-auto">
              <div className="px-3 py-1 text-[10px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100 mb-1">
                Select Compliance Record
              </div>
              {additionalTabs.map((tab) => {
                const isSelected = selectedDocument === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => { setSelectedDocument(tab.id); setShowAdditional(false); }}
                    className={`block w-full text-left px-3 py-1.5 text-xs transition-colors flex items-center justify-between ${
                      isSelected ? 'text-blue-700 font-bold bg-blue-50' : 'text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    <span>{tab.label}</span>
                    {isSelected && <span className="text-blue-600 text-xs">✓</span>}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </nav>
    </div>
  );
}
