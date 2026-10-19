import React, { useState } from 'react';
import { useDashboardStore } from './store/dashboardStore';
import useEscape from './utils/useEscape';
import useDialogFocus from './utils/useDialogFocus';

export default function TenderConfigurator() {
  const [isOpen, setIsOpen]   = useState(false);
  const [file, setFile]       = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);
  const tenderRules    = useDashboardStore(s => s.tenderRules);
  const setTenderRules = useDashboardStore(s => s.setTenderRules);

  useEscape(() => setIsOpen(false), isOpen);
  useDialogFocus(isOpen);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true); setError(null);
    const formData = new FormData();
    formData.append('tender_pdf', file);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')}/api/v1/tenders/tender-custom/compile-rules`, {
        method: 'POST', body: formData,
      });
      if (!res.ok) throw new Error('Failed to compile rules');
      const data = await res.json();
      setTenderRules(data.extracted_rules || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button onClick={() => setIsOpen(true)} className="btn btn-ondark" title="Configure tender rules" aria-label="Configure tender rules">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6" d="M4 7h10M18 7h2M4 17h2M10 17h10M14 4v6M6 14v6" />
        </svg>
        <span className="hidden xl:inline">Configure tender rules</span>
      </button>

      {isOpen && (
        <div className="scrim" onClick={() => setIsOpen(false)}>
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="rules-title"
            onClick={(e) => e.stopPropagation()}
            className="bg-sheet rounded-lg shadow-2xl max-w-2xl w-full overflow-hidden border border-slate-200"
          >
            <div className="px-6 py-4 flex items-start justify-between gap-4 border-b border-slate-100">
              <div>
                <h2 id="rules-title" className="text-[18px] font-medium leading-tight">AI tender rule compiler</h2>
                <p className="text-[13px] text-slate-500 mt-1">
                  Upload an English-language tender PDF. The AI engine extracts the eligibility criteria and
                  turns them into deterministic rules for the bidder verification dashboard.
                </p>
              </div>
              <button onClick={() => setIsOpen(false)} className="btn !h-8 !w-8 !px-0 shrink-0" aria-label="Close">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <div className="px-6 py-5">
              <div className="flex items-center gap-3 mb-5">
                <label className="flex-1 min-w-0">
                  <span className="sr-only">Tender PDF</span>
                  <input type="file" accept="application/pdf"
                    onChange={(e) => setFile(e.target.files[0])}
                    className="block w-full text-[13px] text-slate-600 cursor-pointer border border-slate-300 rounded-md bg-sheet file:mr-3 file:h-9 file:px-3 file:border-0 file:border-r file:border-slate-300 file:bg-slate-100 file:text-[13px] file:font-medium file:text-ink hover:file:bg-slate-200"
                  />
                </label>
                <button onClick={handleUpload} disabled={!file || loading} className="btn btn-lg btn-primary">
                  {loading ? 'Compiling…' : 'Extract rules'}
                </button>
              </div>

              {error && <p className="notice notice-bad mb-4">{error}</p>}

              {tenderRules?.length > 0 && (
                <div>
                  <h3 className="text-[14px] font-medium mb-2">Extracted deterministic rules</h3>
                  <ul className="max-h-60 overflow-y-auto">
                    {tenderRules.map((r, i) => (
                      <li key={i} className="py-3 border-t border-slate-100 first:border-t-0">
                        <div className="text-[14px] font-medium">{r.clause}</div>
                        <div className="text-[14px] text-slate-700 mt-0.5">{r.description}</div>
                        <div className="text-[12px] text-slate-500 font-mono mt-1">Rule ID {r.mapped_regulatory_id}</div>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="px-6 py-3 border-t border-slate-100 bg-slate-50 flex justify-end">
              <button onClick={() => setIsOpen(false)} className="btn btn-lg btn-primary">
                Close and apply to dashboard
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
