import React, { useState } from 'react';
import { useDashboardStore } from './store/dashboardStore';

export default function TenderConfigurator() {
  const [isOpen, setIsOpen] = useState(false);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const tenderRules = useDashboardStore(s => s.tenderRules);
  const setTenderRules = useDashboardStore(s => s.setTenderRules);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('tender_pdf', file);

    try {
      const res = await fetch('http://localhost:8000/api/v1/tenders/tender-custom/compile-rules', {
        method: 'POST',
        body: formData,
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
      <button 
        onClick={() => setIsOpen(true)}
        className="bg-slate-700 hover:bg-slate-600 text-white text-sm font-bold px-4 py-1.5 rounded flex items-center transition shadow-sm"
      >
        <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
        Configure Tender Rules
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-slate-900/70 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full overflow-hidden border border-slate-200">
            <div className="bg-slate-800 px-6 py-4 flex items-center justify-between">
              <div className="flex items-center text-white">
                <svg className="w-5 h-5 text-blue-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                <h3 className="font-bold text-lg">AI Tender Rule Compiler</h3>
              </div>
              <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>

            <div className="p-6">
              <p className="text-sm text-slate-600 mb-4">
                Upload a Tender Document (PDF). The AI Engine will parse the document, extract eligibility criteria, and translate them into deterministic rules for the Bidder Verification Dashboard.
              </p>

              <div className="flex items-center gap-3 mb-6">
                <input 
                  type="file" 
                  accept="application/pdf"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer border border-slate-200 rounded"
                />
                <button 
                  onClick={handleUpload}
                  disabled={!file || loading}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 rounded transition shadow-sm disabled:opacity-50 whitespace-nowrap"
                >
                  {loading ? 'Compiling...' : 'Extract Rules'}
                </button>
              </div>

              {error && <div className="text-red-600 text-sm mb-4 bg-red-50 p-3 rounded">{error}</div>}

              {tenderRules.length > 0 && (
                <div>
                  <h4 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-3">Extracted Deterministic Rules</h4>
                  <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
                    {tenderRules.map((r, i) => (
                      <div key={i} className="bg-emerald-50 border border-emerald-200 rounded p-4">
                        <div className="text-emerald-800 font-bold text-sm mb-1">{r.clause}</div>
                        <div className="text-emerald-900 text-sm mb-2">{r.description}</div>
                        <div className="text-[10px] text-emerald-600 font-mono tracking-tight">System Rule ID: {r.mapped_regulatory_id}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <div className="bg-slate-50 px-6 py-4 border-t border-slate-200 flex justify-end">
              <button onClick={() => setIsOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded transition">
                Close & Apply to Dashboard
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
