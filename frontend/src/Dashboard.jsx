import React, { useState, useEffect } from 'react';
import EvidenceGraph from './EvidenceGraph';
import ContradictionReview from './ContradictionReview';
import GovDocPanel from './GovDocPanel';
import { useDashboardStore } from './store/dashboardStore';

export default function Dashboard({ bidderId }) {
  const tenderRules = useDashboardStore(s => s.tenderRules);
  const verifiedDocResult = useDashboardStore(s => s.verifiedDocResult);
  const clearVerifiedDocResult = useDashboardStore(s => s.clearVerifiedDocResult);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // If a doc was uploaded, don't re-fetch — use that result instead
    if (verifiedDocResult) return;

    async function fetchData() {
      setLoading(true);
      try {
        await fetch(`http://localhost:8000/api/v1/verify/bidder/${bidderId}/tender/tender-sih-2026`, { method: 'POST' });
        const res = await fetch(`http://localhost:8000/api/v1/dashboard/bidder/${bidderId}`);
        if (!res.ok) throw new Error("Failed to fetch dashboard data");
        const json = await res.json();
        setData(json);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [bidderId, tenderRules, verifiedDocResult]);

  // If a bidder PDF was uploaded, use that result instead of the dropdown data
  const displayData = verifiedDocResult || data;
  const displayBidderId = verifiedDocResult ? verifiedDocResult.bidder_id : bidderId;

  if (!verifiedDocResult && loading) return <div className="p-12 text-center text-slate-500 font-medium">Assembling Evidence Provenance Graph...</div>;
  if (!verifiedDocResult && error) return <div className="p-12 text-center text-red-500 font-medium">Error: {error}</div>;
  if (!displayData) return null;

  return (
    <div className="max-w-5xl mx-auto p-6">

      {/* Uploaded Doc Banner */}
      {verifiedDocResult && (
        <div className="mb-4 flex items-center justify-between bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
          <div className="flex items-center gap-2 text-blue-800 text-sm font-medium">
            <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            Showing results from uploaded document: <span className="font-bold">{verifiedDocResult.bidder_id}</span>
            &nbsp;|&nbsp; Extracted claims: {Object.keys(verifiedDocResult.extracted_claims || {}).join(', ')}
          </div>
          <button
            onClick={clearVerifiedDocResult}
            className="ml-4 text-xs text-blue-600 underline hover:text-blue-800 shrink-0"
          >
            ✕ Clear &amp; return to dropdown
          </button>
        </div>
      )}

      {/* Top Header Panel */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 mb-6 p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Bidder Verification Dashboard</h1>
            <p className="text-slate-500 text-sm mt-1">Target: {displayBidderId}</p>
          </div>
          <div className={`px-4 py-2 rounded-full font-bold text-sm tracking-wide ${
            displayData.overall_status === 'VERIFIED_COMPLIANT' ? 'bg-emerald-100 text-emerald-800' :
            'bg-red-600 text-white shadow-lg'
          }`}>
            STATUS: {displayData.overall_status.replace(/_/g, ' ')}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-8">
          {/* Hard Filters */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Hard Filters (Deterministic)</h3>
            <div className="space-y-2">
              {Object.entries(displayData.hard_filters).map(([key, val]) => (
                <div key={key} className="flex items-center justify-between bg-slate-50 p-2 rounded border border-slate-100 text-sm">
                  <span className="text-slate-600 capitalize">{key.replace('_', ' ')}</span>
                  <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wider flex items-center gap-1 ${val === 'PASS' ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' : 'bg-red-100 text-red-700 border border-red-200'}`}>
                    {val === 'PASS' ? (
                      <><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg> VERIFIED</>
                    ) : (
                      <><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M6 18L18 6M6 6l12 12"></path></svg> FAILED</>
                    )}
                  </span>
                </div>
              ))}

              {/* Dynamically Extracted Rules */}
              {tenderRules.length > 0 && (
                <div className="mt-4 pt-4 border-t border-slate-200">
                  <h4 className="text-[10px] font-bold text-blue-500 uppercase tracking-wider mb-2">Tender-Specific Rules (AI Extracted)</h4>
                  {tenderRules.map((rule, idx) => (
                    <div key={idx} className="flex items-center justify-between bg-blue-50 p-2 rounded border border-blue-100 text-sm mb-2">
                      <div className="flex flex-col">
                        <span className="text-blue-800 font-semibold text-xs">{rule.clause}</span>
                        <span className="text-blue-600 text-[10px] truncate max-w-[200px]">{rule.description}</span>
                      </div>
                      <span className="text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wider flex items-center gap-1 bg-emerald-100 text-emerald-700 border border-emerald-200 shrink-0">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg> APPLIED
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
          
          {/* Scores */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Graph Scoring</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Evidence Confidence</span>
                  <span className="font-semibold text-slate-800">{displayData.scores.evidence_confidence} / 1.00</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{width: `${displayData.scores.evidence_confidence * 100}%`}}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Probabilistic Risk</span>
                  <span className="font-semibold text-slate-800">{displayData.scores.probabilistic_risk} / 100</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                  <div className="bg-amber-500 h-2 rounded-full" style={{width: `${displayData.scores.probabilistic_risk}%`}}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <GovDocPanel />

      <EvidenceGraph graphData={displayData.graph_data} />
      
      <ContradictionReview 
        contradictions={displayData.active_contradictions} 
        bidderId={displayBidderId} 
      />
      
    </div>
  );
}
