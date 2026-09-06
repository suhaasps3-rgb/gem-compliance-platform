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

  const tabs = [
    { id: 'tender', label: 'Tender Document' },
    { id: 'gst', label: 'GST Certificate' },
    { id: 'udyam', label: 'Udyam Certificate' },
  ];

  return (
    <div className="border-b border-gray-200 mb-2">
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
    </div>
  );
}
