import React, { useState } from 'react';
import Dashboard from './Dashboard';

function App() {
  const [currentBidder, setCurrentBidder] = useState("bidder-delta-004");
  const [cartelData, setCartelData] = useState(null);
  const [isScanning, setIsScanning] = useState(false);

  const runCartelScan = async () => {
    setIsScanning(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/tenders/tender-sih-2026/collusion-signals');
      const data = await response.json();
      setCartelData(data.investigative_leads);
    } catch (err) {
      alert("Failed to run scan.");
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 font-sans text-slate-800">
      <nav className="bg-slate-900 text-white p-4 flex justify-between items-center shadow-md">
        <div className="font-bold text-xl tracking-tight flex items-center gap-2">
          <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
          GeM Compliance
        </div>
        <div className="flex gap-4 items-center">
          <button 
            onClick={runCartelScan}
            disabled={isScanning}
            className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-bold px-4 py-1.5 rounded flex items-center transition shadow-sm disabled:opacity-50"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            {isScanning ? 'Scanning Network...' : 'Run Anti-Cartel Scan'}
          </button>
          <select 
            value={currentBidder}
            onChange={(e) => setCurrentBidder(e.target.value)}
            className="bg-slate-800 text-white border border-slate-700 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="bidder-acme-001">Acme Corp (Green)</option>
            <option value="bidder-gamma-003">Gamma Tech (Yellow)</option>
            <option value="bidder-delta-004">Delta Solutions (Red Contradiction)</option>
          </select>
          <div className="text-sm font-medium text-slate-300 bg-slate-800 px-3 py-1.5 rounded">
            Officer: Inspector Raj
          </div>
        </div>
      </nav>

      <main className="py-8">
        <Dashboard bidderId={currentBidder} />
      </main>

      {/* Cartel Modal */}
      {cartelData && (
        <div className="fixed inset-0 bg-slate-900/60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-2xl max-w-3xl w-full overflow-hidden border-2 border-red-500">
            <div className="bg-red-600 px-6 py-4 flex items-center justify-between">
              <div className="flex items-center text-white">
                <svg className="w-6 h-6 mr-3 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                <h3 className="font-bold text-xl tracking-wide uppercase">Investigative Lead: Cartelization Detected</h3>
              </div>
              <button onClick={() => setCartelData(null)} className="text-white hover:text-red-200">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>
            
            <div className="p-8">
              {cartelData.length === 0 ? (
                <div className="text-center text-slate-500 py-8 font-medium text-lg">No cross-bidder collisions detected in this tender.</div>
              ) : (
                cartelData.map((lead, idx) => (
                  <div key={idx} className="mb-6 last:mb-0">
                    <div className="flex gap-4 items-center mb-6 justify-center">
                      <div className="bg-slate-100 text-slate-800 font-bold px-6 py-3 rounded-lg border-2 border-slate-300 text-lg shadow-inner">
                        {lead.bidders_involved[0].toUpperCase()}
                      </div>
                      <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
                      <div className="bg-slate-100 text-slate-800 font-bold px-6 py-3 rounded-lg border-2 border-slate-300 text-lg shadow-inner">
                        {lead.bidders_involved[1].toUpperCase()}
                      </div>
                    </div>

                    <div className="bg-red-50 rounded-lg p-5 border border-red-200 mb-6">
                      <h4 className="text-sm font-bold text-red-800 uppercase tracking-wider mb-3">Hard Evidence Intersections</h4>
                      <ul className="space-y-3">
                        {lead.evidence.map((ev, eIdx) => (
                          <li key={eIdx} className="flex items-start text-red-900">
                            <svg className="w-5 h-5 text-red-500 mr-2 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
                            <span className="font-medium">{ev}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="bg-slate-900 text-slate-300 p-4 rounded-lg text-sm border-l-4 border-yellow-500 font-mono">
                      <span className="text-yellow-500 font-bold">LEGAL GUARDRAIL:</span> {lead.disclaimer}
                    </div>
                  </div>
                ))
              )}
            </div>
            
            <div className="bg-slate-50 px-6 py-4 border-t border-slate-200 flex justify-end">
              <button className="bg-red-600 hover:bg-red-700 text-white font-bold px-6 py-2.5 rounded transition flex items-center shadow-md">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                Escalate to Vigilance Dept
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
