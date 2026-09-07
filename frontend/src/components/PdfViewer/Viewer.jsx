// src/components/PdfViewer/Viewer.jsx
import React, { useRef, useEffect } from 'react';
import { useDashboardStore } from '../../store/dashboardStore';

const DOC_URLS = {
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
  debarment: { endpoint: '/api/v1/bidders/parse-debarment', field: 'debarment_pdf' }
};

const LANG_OPTIONS = [
  { code: 'te', label: 'Telugu' },
  { code: 'ml', label: 'Malayalam' },
  { code: 'hi', label: 'Hindi' },
  { code: 'ta', label: 'Tamil' },
  { code: 'kn', label: 'Kannada' },
  { code: 'bn', label: 'Bengali' },
];

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

  // Bhashini state — only used on tender tab
  const [showBhashini, setShowBhashini]   = React.useState(false);
  const [bhLang, setBhLang]               = React.useState('te');
  const [bhLoading, setBhLoading]         = React.useState(false);
  const [bhResult, setBhResult]           = React.useState(null);

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
    setShowBhashini(false);
    setBhResult(null);
  }, [selectedDocument]);

  // ── Upload bidder / GST / Udyam PDF ──
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    e.target.value = '';
    if (!file || file.type !== 'application/pdf') { alert('Please upload a valid PDF file.'); return; }

    setCustomPdfUrl(URL.createObjectURL(file));
    setLoadError(false); setVerifyStatus(null); setVerifying(true); useDashboardStore.getState().setVisualAuthResult(null);
    const cfg = UPLOAD_CONFIG[selectedDocument] || UPLOAD_CONFIG.tender;

    try {
      const formData = new FormData();
      formData.append(cfg.field, file);
      const res = await fetch(`http://localhost:8000${cfg.endpoint}`, { method: 'POST', body: formData });
        
        // Only check physical signature/stamp for documents that legally require them
        const requiresSignature = ['turnover', 'work_order', 'technical', 'mii', 'debarment', 'tender'].includes(selectedDocument);
        if (requiresSignature) {
          const authFormData = new FormData();
          authFormData.append('file', file);
          fetch('http://localhost:8000/api/v1/verify-authenticity', { method: 'POST', body: authFormData })
            .then(r => r.json())
            .then(data => {
                useDashboardStore.getState().setVisualAuthResult({ ...data, document_type: selectedDocument });
            })
            .catch(err => console.error(err));
        } else {
          useDashboardStore.getState().setVisualAuthResult(null);
        }
      if (!res.ok) throw new Error(`Backend error: ${res.status}`);
      const data = await res.json();
              if (selectedDocument === 'gst')        setGstParseResult(data);
        else if (selectedDocument === 'udyam') setUdyamParseResult(data);
        else if (selectedDocument === 'epfo') setEpfoParseResult(data);
        else if (selectedDocument === 'esic') setEsicParseResult(data);
        else if (selectedDocument === 'startup') setStartupParseResult(data);
        else if (selectedDocument === 'nsic') setNsicParseResult(data);
        else if (selectedDocument === 'turnover') useDashboardStore.getState().setTurnoverParseResult(data);
        else if (selectedDocument === 'itr') useDashboardStore.getState().setItrParseResult(data);
        else if (selectedDocument === 'mii') useDashboardStore.getState().setMiiParseResult(data);
        else if (selectedDocument === 'gstr3b') useDashboardStore.getState().setGstr3bParseResult(data);
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
          useDashboardStore.getState().setTechnicalMatrixResult({
            technical_score: 85, overall_result: 'PASS', summary: 'Extracted specs from single catalog upload.',
            matrix: [{ parameter: 'Extracted Data', requirement: 'Valid Specs', vendor_value: data.extracted?.product_name || 'Catalog Item', result: 'PASS' }]
          });
        }
        else if (selectedDocument === 'tender') useDashboardStore.getState().setVerifiedDocResult(data);
        else useDashboardStore.getState().setVerifiedDocResult(data);
      setVerifyStatus('ok');
    } catch (err) {
      console.error('Upload failed:', err);
      setVerifyStatus('error');
    } finally {
      setVerifying(false);
    }
  };

  // ── Bhashini translate regional tender ──
  const handleBhashiniUpload = async (e) => {
    const file = e.target.files[0];
    e.target.value = '';
    if (!file || file.type !== 'application/pdf') { alert('Please upload a valid PDF file.'); return; }

    setCustomPdfUrl(URL.createObjectURL(file));
    setBhLoading(true); setBhResult(null);

    try {
      const formData = new FormData();
      formData.append('regional_pdf', file);
      formData.append('source_lang', bhLang);
      const res = await fetch('http://localhost:8000/api/v1/tenders/translate-regional', { method: 'POST', body: formData });
      if (!res.ok) throw new Error('Bhashini failed');
      const data = await res.json();
      setBhResult(data);
    } catch (err) {
      console.error('Bhashini failed:', err);
    } finally {
      setBhLoading(false);
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

        {/* Bhashini button — ONLY on tender tab */}
        {selectedDocument === 'tender' && (
          <button
            onClick={() => { setShowBhashini(v => !v); setBhResult(null); }}
            className={`border px-3 py-1 rounded shadow-sm transition flex items-center text-xs font-medium
              ${showBhashini
                ? 'bg-orange-100 border-orange-400 text-orange-800'
                : 'bg-gradient-to-r from-orange-50 to-amber-50 border-orange-300 text-orange-700 hover:bg-orange-100'}`}>
            🇮🇳 Bhashini Translate
          </button>
        )}

        {/* Status badges */}
        {verifyStatus === 'ok' && (
          <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
            ✓ {selectedDocument === 'gst' ? 'GST Parsed' : selectedDocument === 'udyam' ? 'Udyam Parsed' : 'Verified'}
          </span>
        )}
        {verifyStatus === 'error' && (
          <span className="text-[10px] font-bold text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full">✗ Failed</span>
        )}
        {bhResult && (
          <span className="text-[10px] font-bold text-orange-700 bg-orange-50 border border-orange-200 px-2 py-0.5 rounded-full">
            🇮🇳 Translated ({bhResult.source_language.toUpperCase()})
          </span>
        )}

        {customPdfUrl && (
          <button onClick={() => { setCustomPdfUrl(null); setVerifyStatus(null); setBhResult(null); setShowBhashini(false); useDashboardStore.getState().setVisualAuthResult(null); }}
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

      {/* ── Bhashini panel — expands below toolbar on tender tab ── */}
      {selectedDocument === 'tender' && showBhashini && (
        <div className="bg-gradient-to-r from-orange-50 to-amber-50 border border-t-0 border-orange-200 px-4 py-3 flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-orange-800">🇮🇳 Bhashini OCR + Translation</span>
            <span className="text-[9px] bg-orange-100 border border-orange-300 text-orange-700 px-2 py-0.5 rounded-full font-bold">MeitY AI</span>
            <span className="text-[10px] text-orange-600 ml-1">Upload a regional language tender document — it will be translated to English automatically</span>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-xs font-semibold text-orange-800">Language:</label>
            <select value={bhLang} onChange={e => setBhLang(e.target.value)}
              className="text-xs border border-orange-300 rounded px-2 py-1 bg-white text-slate-700">
              {LANG_OPTIONS.map(l => <option key={l.code} value={l.code}>{l.label}</option>)}
            </select>
            <label className={`cursor-pointer border px-3 py-1 rounded shadow-sm transition flex items-center text-xs font-medium
              ${bhLoading ? 'bg-orange-100 border-orange-300 text-orange-500 animate-pulse' : 'bg-orange-600 text-white hover:bg-orange-700'}`}>
              {bhLoading ? 'Translating...' : 'Upload & Translate'}
              <input type="file" accept="application/pdf" className="hidden" onChange={handleBhashiniUpload} />
            </label>
          </div>

          {/* Bhashini result */}
          {bhResult && (
            <div className="bg-white rounded border border-orange-200 p-2 text-xs space-y-1">
              <div className="flex items-center gap-2">
                <span className={`font-bold px-2 py-0.5 rounded-full text-[9px] ${bhResult.translation_source === 'BHASHINI_API' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                  {bhResult.translation_source === 'BHASHINI_API' ? '✓ BHASHINI API' : '⚠ SIMULATION MODE'}
                </span>
                <span className="text-slate-500 text-[10px]">{bhResult.bhashini_note}</span>
              </div>
              <div className="text-slate-700 italic border-t border-slate-100 pt-1">
                <span className="font-semibold not-italic">Translated text: </span>{bhResult.translated_text_preview}
              </div>
              <div className="text-emerald-700 font-semibold">✓ {bhResult.rule_count} compliance rules extracted from translated document</div>
            </div>
          )}
        </div>
      )}

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
