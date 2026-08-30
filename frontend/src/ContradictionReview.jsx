import React, { useState } from 'react';

export default function ContradictionReview({ contradictions, bidderId }) {
  const [loading, setLoading] = useState(false);
  const [modalData, setModalData] = useState(null);

  if (!contradictions || contradictions.length === 0) {
    return (
      <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-6 flex items-center justify-center text-emerald-700">
        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
        <span className="font-semibold text-lg">Verified: No Conflicts Found</span>
      </div>
    );
  }

  const handleShowCause = async (contradiction) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/officer/decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bidder_id: bidderId,
          contradiction_id: contradiction.contradiction_id,
          action: "GENERATE_SHOW_CAUSE",
          rule_citation_id: "uuid-for-GFR-175",
          escalation_flag_id: "uuid-for-GFR-151",
          justification: contradiction.ai_synthesis
        })
      });
      const data = await response.json();
      setModalData(data);
    } catch (err) {
      alert("Failed to submit decision.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {contradictions.map((conflict, idx) => (
        <div key={idx} className="bg-white border-2 border-red-200 rounded-lg shadow-sm overflow-hidden relative">
          <div className="bg-red-50 border-b border-red-100 px-6 py-4 flex items-center">
            <svg className="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            <h2 className="text-red-800 font-bold text-lg">Contradiction Detected</h2>
          </div>
          
          <div className="p-6">
            <div className="grid grid-cols-2 gap-6 mb-6">
              {/* Claim Panel */}
              <div className="bg-slate-50 border border-slate-200 rounded p-4">
                <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Claimed Evidence</div>
                <div className="text-slate-800 font-mono text-sm">{conflict.claim}</div>
              </div>
              
              {/* Evidence Panel */}
              <div className="bg-amber-50 border border-amber-200 rounded p-4">
                <div className="text-xs font-bold text-amber-700 uppercase tracking-wider mb-2">Authoritative Government Data</div>
                <div className="text-amber-900 font-mono text-sm">{conflict.evidence}</div>
              </div>
            </div>

            {/* AI Synthesis */}
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6 text-blue-900 text-sm">
              <span className="font-bold mr-2">AI Synthesis:</span>
              {conflict.ai_synthesis}
            </div>

            {/* Action Buttons */}
            <div className="flex justify-end gap-3 border-t border-slate-100 pt-4">
              <button className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-50 rounded transition">
                Dismiss (Manual Override)
              </button>
              <button 
                onClick={() => handleShowCause(conflict)}
                disabled={loading}
                className="bg-red-600 hover:bg-red-700 text-white font-medium px-6 py-2 rounded transition shadow-sm disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Generate Show-Cause Notice'}
              </button>
            </div>
          </div>
        </div>
      ))}

      {/* Modal Overlay */}
      {modalData && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full overflow-hidden">
            <div className="bg-slate-900 px-6 py-4 flex items-center justify-between">
              <div className="flex items-center text-white">
                <svg className="w-5 h-5 text-emerald-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                <h3 className="font-bold text-lg">Statutory Action Recorded</h3>
              </div>
              <button onClick={() => setModalData(null)} className="text-slate-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>
            
            <div className="p-6">
              <div className="mb-6">
                <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">SHA-256 Audit Hash (Tamper-Evident Ledger)</div>
                <div className="bg-slate-100 p-3 rounded font-mono text-xs text-slate-700 break-all border border-slate-200">
                  {modalData.audit_hash}
                </div>
              </div>
              
              <div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Generated Notice Text (GFR 175)</div>
                <div className="bg-amber-50 p-4 rounded text-sm text-amber-900 font-serif border border-amber-200 whitespace-pre-wrap">
                  {modalData.generated_notice_text}
                </div>
              </div>
            </div>
            
            <div className="bg-slate-50 px-6 py-4 border-t border-slate-200 flex justify-end gap-3">
              <button onClick={() => setModalData(null)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded transition">
                Close
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded transition flex items-center">
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                Download PDF
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
