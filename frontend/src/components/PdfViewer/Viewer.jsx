// src/components/PdfViewer/Viewer.jsx
import React, { useRef, useEffect } from 'react';
import { useDashboardStore } from '../../store/dashboardStore';

const DOC_URLS = {
  tender: '/tender_demo.pdf',
  gst:    '/gst_demo.pdf',
  udyam:  '/udyam_demo.pdf',
  epfo: '/epfo_demo.pdf',
  esic: '/esic_demo.pdf',
  startup: '/startup_india_demo.pdf',
  nsic: '/nsic_demo.pdf',
  work_order: '/work_order_1.pdf',
  turnover: '/ca_turnover.pdf',
  technical: '/technical_catalog.pdf',
  itr: '/tender_demo.pdf',
  mii: '/tender_demo.pdf',
  gstr3b: '/gstr3b_demo.pdf',
  debarment: '/debarment_demo.pdf'
};

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
  debarment: { endpoint: '/api/v1/bidders/parse-debarment', field: 'debarment_pdf' },
  technical: { endpoint: '/api/v1/bidders/parse-technical', field: 'tech_pdf' }
};

export default function Viewer() {
  const selectedDocument    = useDashboardStore((s) => s.selectedDocument);
  const setViewerRef        = useDashboardStore((s) => s.setViewerRef);
  const setVerifiedDocResult  = useDashboardStore((s) => s.setVerifiedDocResult);
  const setGstParseResult   = useDashboardStore((s) => s.setGstParseResult);
  const setUdyamParseResult = useDashboardStore((s) => s.setUdyamParseResult);
  const setEpfoParseResult = useDashboardStore((s) => s.setEpfoParseResult);
  const setEsicParseResult = useDashboardStore((s) => s.setEsicParseResult);
  const setStartupParseResult = useDashboardStore((s) => s.setStartupParseResult);
  const setNsicParseResult = useDashboardStore((s) => s.setNsicParseResult);

  const iframeRef = useRef(null);
  const [loadError, setLoadError]         = React.useState(false);
  const [customPdfUrl, setCustomPdfUrl]   = React.useState(null);
  const [verifying, setVerifying]         = React.useState(false);
  const [verifyStatus, setVerifyStatus]   = React.useState(null);
  const visualAuthResult = useDashboardStore((s) => s.visualAuthResult);

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

  const pdfUrl = customPdfUrl || DOC_URLS[selectedDocument] || DOC_URLS.tender;

  useEffect(() => {
    setViewerRef({ goToPage: (page) => {
      try { iframeRef.current?.contentWindow?.postMessage({ type: 'goToPage', page }, '*'); } catch (_) {}
    }});
  }, [setViewerRef]);

  useEffect(() => {
    setLoadError(false);
    setCustomPdfUrl(null);
    setVerifyStatus(null);
  }, [selectedDocument]);

  // ── Upload bidder / GST / Udyam PDF ──
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    e.target.value = '';
    if (!file || file.type !== 'application/pdf') { alert('Please upload a valid PDF file.'); return; }

    setCustomPdfUrl(URL.createObjectURL(file));
    setLoadError(false); setVerifyStatus(null); setVerifying(true);
    useDashboardStore.getState().setVisualAuthResult(null);

    const cfg = UPLOAD_CONFIG[selectedDocument] || UPLOAD_CONFIG.tender;
    const requiresSignature = ['turnover', 'work_order', 'technical', 'mii', 'debarment', 'tender'].includes(selectedDocument);

    // STEP 1: Always run visual authenticity check FIRST for docs that need a signature
    if (requiresSignature) {
      try {
        const authFormData = new FormData();
        authFormData.append('file', file);
        const authRes = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/verify-authenticity`, { method: 'POST', body: authFormData });
        if (authRes.ok) {
          const authData = await authRes.json();
          // Set immediately so the dashboard shows the warning right away
          useDashboardStore.getState().setVisualAuthResult({ ...authData, document_type: selectedDocument });
        }
      } catch (authErr) {
        console.error('Visual auth check failed (backend may be offline):', authErr);
        alert('⚠️ Backend is offline. Please wait and try again.');
        setVerifyStatus('error');
        setVerifying(false);
        return;
      }
    } else {
      useDashboardStore.getState().setVisualAuthResult(null);
    }

    // STEP 2: Run the parse endpoint
    try {
      const formData = new FormData();
      formData.append(cfg.field, file);
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${cfg.endpoint}`, { method: 'POST', body: formData });
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const data = await res.json();

      // If parse endpoint also returns visual_auth, use it (more authoritative)
      if (data.visual_auth) {
        useDashboardStore.getState().setVisualAuthResult({ ...data.visual_auth, document_type: selectedDocument });
      }

           if (selectedDocument === 'gst')        setGstParseResult(data);
      else if (selectedDocument === 'udyam')    setUdyamParseResult(data);
      else if (selectedDocument === 'epfo')     setEpfoParseResult(data);
      else if (selectedDocument === 'esic')     setEsicParseResult(data);
      else if (selectedDocument === 'startup')  setStartupParseResult(data);
      else if (selectedDocument === 'nsic')     setNsicParseResult(data);
      else if (selectedDocument === 'turnover') useDashboardStore.getState().setTurnoverParseResult(data);
      else if (selectedDocument === 'itr')      useDashboardStore.getState().setItrParseResult(data);
      else if (selectedDocument === 'mii')      useDashboardStore.getState().setMiiParseResult(data);
      else if (selectedDocument === 'gstr3b')   useDashboardStore.getState().setGstr3bParseResult(data);
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
        useDashboardStore.getState().setTechnicalMatrixResult(data);
      }
      else if (selectedDocument === 'tender') useDashboardStore.getState().setVerifiedDocResult(data);
      else useDashboardStore.getState().setVerifiedDocResult(data);

      setVerifyStatus('ok');
    } catch (err) {
      console.error('Upload parse failed:', err);
      setVerifyStatus('error');
    } finally {
      setVerifying(false);
    }
  };

  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center h-96 bg-gray-50 rounded border border-gray-200 text-gray-600">
        <p className="text-sm font-medium mb-3">Could not load PDF</p>
        <a href={pdfUrl} target="_blank" rel="noreferrer" className="text-blue-600 underline text-sm">⬇ Download PDF instead</a>
        <button onClick={() => setLoadError(false)} className="mt-2 text-xs text-gray-500 underline">Retry</button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* ── Toolbar ── */}
      <div className="flex items-center flex-wrap gap-2 bg-slate-100 border border-slate-200 rounded-t px-3 py-2 text-xs text-slate-700">
        <span className="font-semibold text-slate-800">PDF Preview</span>

        {/* Upload button */}
        <label className={`cursor-pointer border px-3 py-1 rounded shadow-sm transition flex items-center text-xs font-medium
          ${verifying ? 'bg-blue-50 border-blue-300 text-blue-600 animate-pulse' :
            selectedDocument === 'gst'   ? 'bg-orange-50 border-orange-300 text-orange-700 hover:bg-orange-100' :
            selectedDocument === 'udyam' ? 'bg-emerald-50 border-emerald-300 text-emerald-700 hover:bg-emerald-100' :
            'bg-white border-slate-300 text-slate-700 hover:bg-slate-50'}`}>
          <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          {getUploadLabel()}
          <input type="file" accept="application/pdf" className="hidden" onChange={handleFileUpload} />
        </label>

        {/* Status badges */}
        {verifyStatus === 'ok' && !visualAuthResult && (
          <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
            ✓ {selectedDocument === 'gst' ? 'GST Parsed' : selectedDocument === 'udyam' ? 'Udyam Parsed' : 'Verified'}
          </span>
        )}
        {verifyStatus === 'ok' && visualAuthResult?.is_signed_and_stamped && (
          <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
            ✓ Signed &amp; Verified
          </span>
        )}
        {visualAuthResult && !visualAuthResult.is_signed_and_stamped && (
          <span className="text-[10px] font-bold text-orange-600 bg-orange-50 border border-orange-200 px-2 py-0.5 rounded-full">
            ⚠ Unsigned — See Dashboard
          </span>
        )}
        {verifyStatus === 'error' && !visualAuthResult && (
          <span className="text-[10px] font-bold text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full">✗ Upload Failed</span>
        )}

        {customPdfUrl && (
          <button onClick={() => { setCustomPdfUrl(null); setVerifyStatus(null); useDashboardStore.getState().setVisualAuthResult(null); }}
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
        style={{ minHeight: '72vh' }}
        onError={() => setLoadError(true)}
      />
    </div>
  );
}
