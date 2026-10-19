// src/components/PdfViewer/DocumentTabs.jsx
import React from 'react';
import { useDashboardStore } from '../../store/dashboardStore';
import useEscape from '../../utils/useEscape';

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
    { id: 'tender', label: 'Tender document' },
    { id: 'gst', label: 'GST certificate' },
    { id: 'udyam', label: 'Udyam certificate' },
  ];

  const [showAdditional, setShowAdditional] = React.useState(false);
  useEscape(() => setShowAdditional(false), showAdditional);

  const additionalTabs = [
    { id: 'epfo', label: 'EPFO statement' },
    { id: 'esic', label: 'ESIC challan' },
    { id: 'startup', label: 'Startup India' },
    { id: 'nsic', label: 'NSIC certificate' },
    { id: 'work_order', label: 'Work order' },
    { id: 'turnover', label: 'CA turnover' },
    { id: 'technical', label: 'Tech catalog' },
    { id: 'itr', label: 'ITR return' },
    { id: 'mii', label: 'MII declaration' },
    { id: 'gstr3b', label: 'GSTR-3B return' },
    { id: 'debarment', label: 'Debarment decl.' }
  ];

  const activeAdditional = additionalTabs.find(t => t.id === selectedDocument);

  const tabClass = (active) =>
    `relative h-10 px-1 mr-4 text-[13px] whitespace-nowrap transition-colors border-b-2 -mb-px ${
      active
        ? 'text-ink font-medium border-ink'
        : 'text-slate-500 hover:text-ink border-transparent'
    }`;

  return (
    <div className="border-b border-slate-200 mb-3 shrink-0">
      <nav className="flex flex-wrap items-end" aria-label="Documents">
        {mainTabs.map((tab) => {
          const isActive = selectedDocument === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setSelectedDocument(tab.id)}
              aria-current={isActive ? 'page' : undefined}
              className={tabClass(isActive)}
            >
              {tab.label}
            </button>
          );
        })}

        <div className="relative">
          <button
            onClick={() => setShowAdditional(!showAdditional)}
            aria-expanded={showAdditional}
            aria-haspopup="menu"
            className={`${tabClass(!!activeAdditional)} inline-flex items-center gap-1.5`}
          >
            <span>{activeAdditional ? activeAdditional.label : 'More statutory documents'}</span>
            <svg className={`w-3 h-3 transition-transform ${showAdditional ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {showAdditional && (
            <div
              role="menu"
              className="absolute top-full left-0 mt-1 bg-sheet border border-slate-200 rounded-lg shadow-xl z-50 w-56 py-1 max-h-72 overflow-y-auto"
            >
              {additionalTabs.map((tab) => {
                const isSelected = selectedDocument === tab.id;
                return (
                  <button
                    key={tab.id}
                    role="menuitem"
                    onClick={() => { setSelectedDocument(tab.id); setShowAdditional(false); }}
                    className={`w-full text-left px-3 h-8 text-[13px] transition-colors flex items-center justify-between ${
                      isSelected ? 'text-ink font-medium bg-slate-100' : 'text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    <span>{tab.label}</span>
                    {isSelected && (
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
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
