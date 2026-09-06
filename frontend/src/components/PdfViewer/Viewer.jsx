// src/components/PdfViewer/Viewer.jsx
import React, { useRef, useEffect } from 'react';
import { useDashboardStore } from '../../store/dashboardStore';

const DOC_URLS = {
  tender: '/tender_demo.pdf',
  gst: '/gst_tender_demo.pdf',
  udyam: '/udyam_tender_demo.pdf',
};

// Which backend endpoint + form field name to use per tab
const UPLOAD_CONFIG = {
  tender: { endpoint: '/api/v1/bidders/verify-document',  field: 'bidder_pdf' },
  gst:    { endpoint: '/api/v1/bidders/parse-gst',         field: 'gst_pdf'    },
  udyam:  { endpoint: '/api/v1/bidders/parse-udyam',       field: 'udyam_pdf'  },
};

export default function Viewer() {
  const selectedDocument   = useDashboardStore((s) => s.selectedDocument);
  const setViewerRef       = useDashboardStore((s) => s.setViewerRef);
  const setVerifiedDocResult = useDashboardStore((s) => s.setVerifiedDocResult);
  const setGstParseResult  = useDashboardStore((s) => s.setGstParseResult);
  const setUdyamParseResult = useDashboardStore((s) => s.setUdyamParseResult);

  const iframeRef = useRef(null);
  const [loadError, setLoadError]     = React.useState(false);
  const [customPdfUrl, setCustomPdfUrl] = React.useState(null);
  const [verifying, setVerifying]     = React.useState(false);
  const [verifyStatus, setVerifyStatus] = React.useState(null); // 'ok' | 'error'

  const pdfUrl = customPdfUrl || DOC_URLS[selectedDocument] || DOC_URLS.tender;

  useEffect(() => {
    setViewerRef({
      goToPage: (page) => {
        if (iframeRef.current) {
          try { iframeRef.current.contentWindow?.postMessage({ type: 'goToPage', page }, '*'); } catch (_) {}
        }
      },
    });
  }, [setViewerRef]);

  useEffect(() => {
    setLoadError(false);
    setCustomPdfUrl(null);
    setVerifyStatus(null);
  }, [selectedDocument]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    // Reset input so same file can be re-uploaded
    e.target.value = '';
    if (!file || file.type !== 'application/pdf') {
      alert('Please upload a valid PDF file.');
      return;
    }

    setCustomPdfUrl(URL.createObjectURL(file));
    setLoadError(false);
    setVerifyStatus(null);
    setVerifying(true);

    const cfg = UPLOAD_CONFIG[selectedDocument] || UPLOAD_CONFIG.tender;

    try {
      const formData = new FormData();
      formData.append(cfg.field, file);

      const res = await fetch(`http://localhost:8000${cfg.endpoint}`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const data = await res.json();

      // Route result to the correct store slice
      if (selectedDocument === 'gst')   setGstParseResult(data);
      else if (selectedDocument === 'udyam') setUdyamParseResult(data);
      else setVerifiedDocResult(data);

      setVerifyStatus('ok');
    } catch (err) {
      console.error('Upload failed:', err);
      setVerifyStatus('error');
    } finally {
      setVerifying(false);
    }
  };

  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center h-96 bg-gray-50 rounded border border-gray-200 text-gray-600">
        <svg className="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p className="text-sm font-medium mb-3">Could not load PDF</p>
        <a
          href={pdfUrl}
          target="_blank"
          rel="noreferrer"
          className="text-blue-600 underline text-sm hover:text-blue-800"
        >
          ⬇ Download PDF instead
        </a>
        <button
          onClick={() => setLoadError(false)}
          className="mt-2 text-xs text-gray-500 underline"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 bg-slate-100 border border-slate-200 rounded-t px-3 py-2 text-xs text-slate-700">
        <span className="font-semibold text-slate-800">PDF Preview</span>

        {/* Upload Button — label changes per tab */}
        <label className={`ml-4 cursor-pointer border px-3 py-1 rounded shadow-sm transition flex items-center text-xs font-medium
          ${verifying ? 'bg-blue-50 border-blue-300 text-blue-600 animate-pulse' :
            selectedDocument === 'gst'   ? 'bg-orange-50 border-orange-300 text-orange-700 hover:bg-orange-100' :
            selectedDocument === 'udyam' ? 'bg-emerald-50 border-emerald-300 text-emerald-700 hover:bg-emerald-100' :
            'bg-white border-slate-300 text-slate-700 hover:bg-slate-50'}`}>
          <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          {verifying ? 'Parsing...' :
           selectedDocument === 'gst'   ? 'Upload GST Certificate' :
           selectedDocument === 'udyam' ? 'Upload Udyam Certificate' :
           'Upload Bidder Document'}
          <input type="file" accept="application/pdf" className="hidden" onChange={handleFileUpload} />
        </label>

        {/* Status badges */}
        {verifyStatus === 'ok' && (
          <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
            ✓ {selectedDocument === 'gst' ? 'GST Parsed' : selectedDocument === 'udyam' ? 'Udyam Parsed' : 'Verified'}
          </span>
        )}
        {verifyStatus === 'error' && (
          <span className="text-[10px] font-bold text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full">✗ Failed</span>
        )}

        {customPdfUrl && (
          <button onClick={() => { setCustomPdfUrl(null); setVerifyStatus(null); }}
            className="text-red-500 hover:text-red-700 underline ml-1 text-xs">
            Clear Upload
          </button>
        )}

        <span className="ml-auto">
          <a href={pdfUrl} target="_blank" rel="noreferrer"
            className="text-blue-600 font-medium hover:text-blue-800 flex items-center text-xs">
            Open full ↗
          </a>
        </span>
      </div>

      {/* PDF iframe */}
      <iframe
        ref={iframeRef}
        src={pdfUrl}
        title="PDF Viewer"
        className="w-full flex-1 rounded-b border border-t-0 border-slate-200"
        style={{ minHeight: '75vh' }}
        onError={() => setLoadError(true)}
      />
    </div>

  );
}
