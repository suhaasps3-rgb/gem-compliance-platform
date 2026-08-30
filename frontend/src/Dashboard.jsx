import React, { useState, useEffect } from 'react';
import EvidenceGraphPlaceholder from './EvidenceGraphPlaceholder';
import ContradictionReview from './ContradictionReview';

export default function Dashboard({ bidderId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        // First trigger verification
        await fetch(`http://localhost:8000/api/v1/verify/bidder/${bidderId}/tender/tender-sih-2026`, { method: 'POST' });
        
        // Then fetch dashboard data
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
  }, [bidderId]);

  if (loading) return <div className="p-12 text-center text-slate-500 font-medium">Assembling Evidence Provenance Graph...</div>;
  if (error) return <div className="p-12 text-center text-red-500 font-medium">Error: {error}</div>;
  if (!data) return null;

  return (
    <div className="max-w-5xl mx-auto p-6">
      
      {/* Top Header Panel */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 mb-6 p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Bidder Verification Dashboard</h1>
            <p className="text-slate-500 text-sm mt-1">Target: {bidderId}</p>
          </div>
          <div className={`px-4 py-2 rounded-full font-bold text-sm tracking-wide ${
            data.overall_status === 'VERIFIED_COMPLIANT' ? 'bg-emerald-100 text-emerald-800' : 
            data.overall_status === 'NEEDS_REVIEW' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'
          }`}>
            STATUS: {data.overall_status.replace('_', ' ')}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-8">
          {/* Hard Filters */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Hard Filters (Deterministic)</h3>
            <div className="space-y-2">
              {Object.entries(data.hard_filters).map(([key, val]) => (
                <div key={key} className="flex items-center justify-between bg-slate-50 p-2 rounded border border-slate-100 text-sm">
                  <span className="text-slate-600 capitalize">{key.replace('_', ' ')}</span>
                  <span className={`font-semibold ${val === 'PASS' ? 'text-emerald-600' : 'text-red-600'}`}>{val}</span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Scores */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Graph Scoring</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Evidence Confidence</span>
                  <span className="font-semibold text-slate-800">{data.scores.evidence_confidence} / 1.00</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{width: `${data.scores.evidence_confidence * 100}%`}}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Probabilistic Risk</span>
                  <span className="font-semibold text-slate-800">{data.scores.probabilistic_risk} / 100</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                  <div className="bg-amber-500 h-2 rounded-full" style={{width: `${data.scores.probabilistic_risk}%`}}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <EvidenceGraphPlaceholder graphData={data.graph_data} />
      
      <ContradictionReview 
        contradictions={data.active_contradictions} 
        bidderId={bidderId} 
      />
      
    </div>
  );
}
