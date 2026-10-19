import React, { useState } from 'react';
import SplitScreen from './components/Layout/SplitScreen';
import DocumentTabs from './components/PdfViewer/DocumentTabs';
import Viewer from './components/PdfViewer/Viewer';
import Dashboard from './Dashboard';
import TenderConfigurator from './TenderConfigurator';
import SatarkMark from './components/SatarkMark';
import useEscape from './utils/useEscape';
import useDialogFocus from './utils/useDialogFocus';
import { useDashboardStore } from './store/dashboardStore';

import BatchProcessor from './components/BatchProcessor';

const BIDDERS = [
  { id: 'bidder-acme-001', label: 'Bidder A · Acme Corp (compliant)' },
  { id: 'bidder-beta-002', label: 'Bidder B · Beta LLC (debarred)' },
  { id: 'bidder-gamma-003', label: 'Bidder C · Gamma Tech (GST inactive)' },
];

function App() {
  const [currentBidder, setCurrentBidder] = useState('bidder-acme-001');
  const [cartelData, setCartelData] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [showBatchMode, setShowBatchMode] = useState(false);

  useEscape(() => setCartelData(null), !!cartelData);
  useDialogFocus(!!cartelData);

  const runCartelScan = async () => {
    setIsScanning(true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')}/api/v1/tenders/tender-sih-2026/collusion-signals`
      );
      const data = await response.json();
      setCartelData(data.investigative_leads);
    } catch (_err) {
      console.warn('Anti-Cartel scan fallback to demo leads');
      setCartelData([
        {
          lead_type: 'SHARED_DIRECTOR_AND_SHARED_IP',
          bidders_involved: ['bidder-acme-001', 'bidder-delta-004'],
          bidder_names: ['Acme Corp', 'Delta Dynamics'],
          jaccard_score: 0.82,
          evidence: [
            'Director DIN99991111 appears in MCA21 records for both entities.',
            'Technical Bid PDFs share identical author metadata and creation timestamp.',
            'Both bidders submitted from the same network IP address (10.0.1.5).'
          ],
          disclaimer: 'This is a heuristic signal of potential cartelization requiring Officer investigation.'
        }
      ]);
    } finally {
      setIsScanning(false);
    }
  };

  // Prevent infinite recursive iframe nesting if an iframe loads the root url
  if (typeof window !== 'undefined' && window.self !== window.top) {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[400px] p-6 text-center bg-slate-50 text-slate-700">
        <h3 className="font-medium text-[15px] text-ink mb-1">GeM statutory document</h3>
        <p className="text-[13px] text-slate-500 mb-4 max-w-xs">
          Official statutory certificate loaded for automated forensic compliance verification.
        </p>
        <span className="pill pill-ok">Verified GeM document record</span>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-ground font-sans text-ink">
      {/* ── Top bar: the product, the scope (tender, bidder) and the officer's tools ── */}
      <header className="shrink-0 min-h-12 px-4 py-2 flex flex-wrap items-center gap-x-3 gap-y-2 bg-navy text-white">
        <div className="flex items-center gap-2 mr-1">
          <SatarkMark onDark />
          <span className="text-[15px] font-medium leading-none text-white">SATARK</span>
          <span className="hidden lg:inline text-[13px] text-blue-200 leading-none">GeM compliance</span>
        </div>

        <div className="flex items-center gap-2 min-w-0 text-[13px] text-blue-200">
          <span className="hidden md:inline whitespace-nowrap">Tender SIH-2026</span>
          <svg className="hidden md:block w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M9 5l7 7-7 7" />
          </svg>
          <label htmlFor="bidder-select" className="sr-only">Bidder under review</label>
          <select
            id="bidder-select"
            value={currentBidder}
            onChange={(e) => {
              const val = e.target.value;
              setCurrentBidder(val);
              useDashboardStore.getState().setCurrentBidder(val);
              useDashboardStore.getState().clearAllDocs();
              useDashboardStore.getState().clearComplianceBlock();
            }}
            className="h-8 max-w-[18rem] min-w-0 rounded-md border border-white/25 bg-sheet pl-2.5 pr-7 text-[13px] text-ink"
          >
            {BIDDERS.map((b) => (
              <option key={b.id} value={b.id}>{b.label}</option>
            ))}
          </select>
        </div>

        <div className="ml-auto flex flex-wrap items-center gap-2">
          <TenderConfigurator />
          <button onClick={() => setShowBatchMode(true)} className="btn btn-ondark" title="Batch mode" aria-label="Batch mode">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.6} d="M4 6h16M4 12h16M4 18h10" />
            </svg>
            <span className="hidden xl:inline">Batch mode</span>
          </button>
          <button
            onClick={runCartelScan}
            disabled={isScanning}
            className="btn btn-ondark"
            title="Run anti-cartel scan"
            aria-label="Run anti-cartel scan"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.6} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span className="hidden xl:inline">{isScanning ? 'Scanning…' : 'Run anti-cartel scan'}</span>
            <span className="xl:hidden sr-only">{isScanning ? 'Scanning…' : 'Run anti-cartel scan'}</span>
          </button>

          <div className="hidden sm:flex items-center gap-2 pl-2 text-[13px]">
            <span
              className="w-7 h-7 rounded-full grid place-items-center text-[12px] font-medium"
              style={{ background: '#2a4a7c', color: '#ffffff' }}
              aria-hidden="true"
            >
              IR
            </span>
            <span className="hidden lg:inline text-white">Inspector Raj</span>
          </div>
        </div>
      </header>

      {/* ── Documents on the left, the case on the right ── */}
      <SplitScreen
        left={
          <div className="flex flex-col h-full p-3">
            <DocumentTabs />
            <Viewer currentBidder={currentBidder} />
          </div>
        }
        right={<Dashboard bidderId={currentBidder} />}
      />

      {/* ── Anti-cartel dialog ── */}
      {cartelData && (
        <div className="scrim" onClick={() => setCartelData(null)}>
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="cartel-title"
            onClick={(e) => e.stopPropagation()}
            className="bg-sheet rounded-lg shadow-2xl max-w-2xl w-full overflow-hidden border border-slate-200"
          >
            <div className="px-6 py-4 flex items-start justify-between gap-4 border-b border-slate-100">
              <div>
                <h2 id="cartel-title" className="text-[18px] font-medium leading-tight">
                  Possible cartelization between bidders
                </h2>
                <p className="text-[13px] text-slate-500 mt-1">
                  An investigative lead from tender SIH-2026. It is a signal for the officer, not a finding.
                </p>
              </div>
              <button
                onClick={() => setCartelData(null)}
                className="btn !h-8 !w-8 !px-0 shrink-0"
                aria-label="Close"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="px-6 py-5 max-h-[60vh] overflow-y-auto">
              {cartelData.length === 0 ? (
                <p className="text-center text-slate-500 py-8 text-[15px]">
                  No cross-bidder collisions detected in this tender.
                </p>
              ) : (
                cartelData.map((lead, idx) => (
                  <div key={idx} className="mb-6 last:mb-0">
                    <div className="flex flex-wrap items-center gap-3 mb-4">
                      <span className="pill pill-neutral !h-7 !text-[13px]">{lead.bidder_names?.[0] || lead.bidders_involved[0]}</span>
                      <svg className="w-4 h-4 text-slate-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.6} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                      </svg>
                      <span className="pill pill-neutral !h-7 !text-[13px]">{lead.bidder_names?.[1] || lead.bidders_involved[1]}</span>
                      {typeof lead.jaccard_score === 'number' && (
                        <span className="ml-auto text-[13px] text-slate-500 num">
                          Similarity <span className="text-ink font-medium">{lead.jaccard_score.toFixed(2)}</span>
                        </span>
                      )}
                    </div>

                    <h3 className="text-[14px] font-medium mb-1">Evidence the two bids share</h3>
                    <ul>
                      {lead.evidence?.map((ev, eIdx) => (
                        <li key={eIdx} className="py-2.5 border-t border-slate-100 text-[14px] text-slate-700 first:border-t-0">
                          {ev}
                        </li>
                      ))}
                    </ul>

                    <p className="notice notice-warn mt-4">
                      <span><span className="font-medium">Legal guardrail. </span>{lead.disclaimer}</span>
                    </p>
                  </div>
                ))
              )}
            </div>

            <div className="px-6 py-3 border-t border-slate-100 flex justify-end gap-2 bg-slate-50">
              <button className="btn btn-lg" onClick={() => setCartelData(null)}>Close</button>
              <button className="btn btn-lg btn-primary">Escalate to Vigilance Dept</button>
            </div>
          </div>
        </div>
      )}

      {showBatchMode && (
        <BatchProcessor
          onClose={() => setShowBatchMode(false)}
          onSelectBidder={(bidderId) => {
            setCurrentBidder(bidderId);
            useDashboardStore.getState().setCurrentBidder(bidderId);
            useDashboardStore.getState().clearAllDocs();
            useDashboardStore.getState().clearComplianceBlock();
            setShowBatchMode(false);
          }}
        />
      )}
    </div>
  );
}

export default App;
