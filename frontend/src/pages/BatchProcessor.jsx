import React, { useState, useEffect } from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function BatchProcessor() {
  const [file, setFile] = useState(null);
  const [batchId, setBatchId] = useState(null);
  const [status, setStatus] = useState(null); // QUEUED, PROCESSING, COMPLETED, ERROR
  const [progress, setProgress] = useState(0);
  const [summary, setSummary] = useState(null);
  const { setBatchModeActive } = useDashboardStore();

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

  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-75 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-3xl overflow-hidden flex flex-col max-h-[90vh]">
        <div className="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
          <h2 className="text-xl font-bold text-gray-800">Batch Processing Pipeline</h2>
          <button onClick={() => setBatchModeActive(false)} className="text-gray-500 hover:text-gray-800">✕</button>
        </div>
        
        <div className="p-6 overflow-y-auto">
          {!batchId ? (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
              <div className="text-4xl mb-4">📁</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Upload Bidder ZIP Archive</h3>
              <p className="text-sm text-gray-500 mb-6">ZIP file should contain one folder per bidder with their PDFs.</p>
              <input type="file" accept=".zip" onChange={(e) => setFile(e.target.files[0])} className="mb-4 block mx-auto text-sm" />
              <button 
                onClick={handleUpload} 
                disabled={!file}
                className="px-4 py-2 bg-blue-600 text-white font-medium rounded hover:bg-blue-700 disabled:opacity-50"
              >
                Start Processing
              </button>
            </div>
          ) : (
            <div>
              <div className="mb-8">
                <div className="flex justify-between items-end mb-2">
                  <div>
                    <h3 className="font-bold text-gray-800 text-lg">Processing Batch: {batchId}</h3>
                    <p className="text-sm text-gray-500">Status: <span className="font-bold">{status}</span></p>
                  </div>
                  <div className="text-2xl font-black text-blue-600">{progress}%</div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4 mb-4 overflow-hidden">
                  <div className="bg-blue-600 h-4 rounded-full transition-all duration-500" style={{ width: `${progress}%` }}></div>
                </div>
              </div>
              
              {summary && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-green-50 p-4 rounded border border-green-200 text-center">
                    <div className="text-2xl font-bold text-green-700">{summary.low_risk}</div>
                    <div className="text-xs font-semibold text-green-600 uppercase">Low Risk</div>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded border border-yellow-200 text-center">
                    <div className="text-2xl font-bold text-yellow-700">{summary.medium_risk}</div>
                    <div className="text-xs font-semibold text-yellow-600 uppercase">Medium Risk</div>
                  </div>
                  <div className="bg-orange-50 p-4 rounded border border-orange-200 text-center">
                    <div className="text-2xl font-bold text-orange-700">{summary.high_risk}</div>
                    <div className="text-xs font-semibold text-orange-600 uppercase">High Risk</div>
                  </div>
                  <div className="bg-red-50 p-4 rounded border border-red-200 text-center">
                    <div className="text-2xl font-bold text-red-700">{summary.critical_risk}</div>
                    <div className="text-xs font-semibold text-red-600 uppercase">Critical / Fail</div>
                  </div>
                </div>
              )}
              
              {status === "COMPLETED" && (
                <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
                  <p className="text-blue-800 font-medium mb-4">Batch processing complete! {summary?.total} bidders evaluated.</p>
                  <button onClick={() => setBatchModeActive(false)} className="px-4 py-2 bg-white border border-gray-300 text-gray-700 font-medium rounded hover:bg-gray-50 shadow-sm">
                    Return to Dashboard
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
