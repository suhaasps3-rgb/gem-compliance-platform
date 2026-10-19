import React, { useState, useEffect } from 'react';
import { useDashboardStore } from '../store/dashboardStore';
import useEscape from '../utils/useEscape';

// Unused legacy page; the dialog in components/BatchProcessor.jsx is the live one.
export default function BatchProcessor() {
  const [file, setFile] = useState(null);
  const [batchId, setBatchId] = useState(null);
  const [status, setStatus] = useState(null); // QUEUED, PROCESSING, COMPLETED, ERROR
  const [progress, setProgress] = useState(0);
  const [summary, setSummary] = useState(null);
  const { setBatchModeActive } = useDashboardStore();

  useEscape(() => setBatchModeActive(false), true);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("batch_zip", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/batch/upload", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setBatchId(data.batch_id);
      setStatus("QUEUED");
    } catch (e) {
      setStatus("ERROR");
    }
  };

  useEffect(() => {
    let interval;
    if (batchId && status !== "COMPLETED" && status !== "ERROR") {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`http://127.0.0.1:8000/api/v1/batch/${batchId}/status`);
          const data = await res.json();
          setProgress(data.progress_pct);
          setStatus(data.status);
          setSummary(data.summary);
          if (data.status === "COMPLETED") clearInterval(interval);
        } catch(e) {}
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [batchId, status]);

  const cells = summary ? [
    ['Low risk', summary.low_risk],
    ['Medium risk', summary.medium_risk],
    ['High risk', summary.high_risk],
    ['Critical or fail', summary.critical_risk],
  ] : [];

  return (
    <div className="scrim">
      <div role="dialog" aria-modal="true" aria-labelledby="batch-legacy-title" className="bg-sheet rounded-lg shadow-2xl w-full max-w-3xl overflow-hidden flex flex-col max-h-[90vh] border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
          <h2 id="batch-legacy-title" className="text-[18px] font-medium">Batch processing pipeline</h2>
          <button onClick={() => setBatchModeActive(false)} className="btn !h-8 !w-8 !px-0" aria-label="Close">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="p-6 overflow-y-auto">
          {!batchId ? (
            <div className="border border-dashed border-slate-300 rounded-lg p-10 text-center">
              <h3 className="text-[16px] font-medium mb-1">Upload bidder ZIP archive</h3>
              <p className="text-[13px] text-slate-500 mb-5">The ZIP should contain one folder per bidder with their PDFs.</p>
              <input type="file" accept=".zip" onChange={(e) => setFile(e.target.files[0])} className="mb-4 block mx-auto text-[13px]" />
              {status === "ERROR" && <p className="notice notice-bad mb-4">The upload failed. Check that the server is running and try again.</p>}
              <button onClick={handleUpload} disabled={!file} className="btn btn-lg btn-primary">
                Start processing
              </button>
            </div>
          ) : (
            <div>
              <div className="mb-6">
                <div className="flex justify-between items-end mb-2">
                  <div>
                    <h3 className="text-[16px] font-medium">Processing batch {batchId}</h3>
                    <p className="text-[13px] text-slate-500">Status: <span className="text-ink font-medium">{status}</span></p>
                  </div>
                  <div className="text-[30px] leading-none num">{progress}%</div>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                  <div className="bg-data h-1.5 rounded-full transition-[width] duration-500" style={{ width: `${progress}%` }}></div>
                </div>
              </div>

              {summary && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-slate-200 border border-slate-200 rounded-lg overflow-hidden mb-6">
                  {cells.map(([label, n]) => (
                    <div key={label} className="bg-sheet px-4 py-3">
                      <div className="label">{label}</div>
                      <div className="mt-1 text-[24px] leading-tight num">{n}</div>
                    </div>
                  ))}
                </div>
              )}

              {status === "COMPLETED" && (
                <div className="notice flex-wrap justify-between items-center">
                  <p>Batch processing complete. {summary?.total} bidders evaluated.</p>
                  <button onClick={() => setBatchModeActive(false)} className="btn">Return to dashboard</button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
