import React, { useState } from 'react';
import Dashboard from './Dashboard';

function App() {
  const [currentBidder, setCurrentBidder] = useState("bidder-delta-004");

  return (
    <div className="min-h-screen bg-slate-100 font-sans text-slate-800">
      <nav className="bg-slate-900 text-white p-4 flex justify-between items-center shadow-md">
        <div className="font-bold text-xl tracking-tight flex items-center gap-2">
          <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
          GeM Compliance
        </div>
        <div className="flex gap-4">
          <select 
            value={currentBidder}
            onChange={(e) => setCurrentBidder(e.target.value)}
            className="bg-slate-800 text-white border border-slate-700 rounded px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="bidder-acme-001">Acme Corp (Green)</option>
            <option value="bidder-gamma-003">Gamma Tech (Yellow)</option>
            <option value="bidder-delta-004">Delta Solutions (Red Contradiction)</option>
          </select>
          <div className="text-sm font-medium text-slate-300 bg-slate-800 px-3 py-1 rounded">
            Officer: Inspector Raj
          </div>
        </div>
      </nav>

      <main className="py-8">
        <Dashboard bidderId={currentBidder} />
      </main>
    </div>
  );
}

export default App;
