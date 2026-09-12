import React, { useState, useEffect } from 'react';

export default function BatchProcessor({ onClose }) {
  const [file, setFile] = useState(null);
  const [batchId, setBatchId] = useState(null);
  const [status, setStatus] = useState('IDLE');
  const [progress, setProgress] = useState({ processed: 0, total: 0 });
  const [bidders, setBidders] = useState({});
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    let interval;
    if (status === 'PROCESSING' && batchId) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/batch/${batchId}/status`);
          if (res.ok) {
            const data = await res.json();
            
            // we also need the full batch details to get bidder info
            const resDetails = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/batch/${batchId}`);
            if (resDetails.ok) {
                const fullData = await resDetails.json();
                setBidders(fullData.bidders || {});
            }

            setProgress({ processed: data.processed, total: data.total });

            if (data.status === 'COMPLETED' || data.status === 'FAILED') {
              setStatus(data.status);
              clearInterval(interval);
            }
          }
        } catch (e) {
          console.error(e);
        }
      }, 1500);
    }
    return () => clearInterval(interval);
  }, [status, batchId]);

  const handleUpload = async () => {
    if (!file) return;
    setStatus('UPLOADING');
    setErrorMsg('');
    const fd = new FormData();
    fd.append('batch_zip', file);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/batch/upload`, {
        method: 'POST',
        body: fd
      });
      if (!res.ok) throw new Error('Upload failed');
      const data = await res.json();
      setBatchId(data.batch_id);
      setProgress({ processed: 0, total: data.bidder_count });
      setStatus('PROCESSING');
    } catch (e) {
      setStatus('ERROR');
      setErrorMsg(e.message);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/70 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full flex flex-col h-[80vh] overflow-hidden border-2 border-purple-500">
        
        <div className="bg-purple-600 px-6 py-4 flex items-center justify-between shrink-0">
          <div className="flex items-center text-white">
            <span className="text-2xl mr-3">⚡</span>
            <h3 className="font-bold text-xl tracking-wide uppercase">Batch Mode: Pipeline Processing</h3>
          </div>
          <button onClick={onClose} className="text-white hover:text-purple-200">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="p-6 flex-1 overflow-y-auto bg-slate-50">
          
          {status === 'IDLE' && (
            <div className="text-center py-12">
              <div className="border-4 border-dashed border-slate-300 rounded-xl p-12 bg-white max-w-xl mx-auto">
                <div className="text-5xl mb-4">🗂️</div>
                <h4 className="text-lg font-bold text-slate-700 mb-2">Upload Batch ZIP</h4>
                <p className="text-slate-500 text-sm mb-6">ZIP file should contain folders for each bidder.</p>
                <input type="file" accept=".zip" onChange={(e) => setFile(e.target.files[0])} className="mb-4 block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100" />
                <button 
                  onClick={handleUpload}
                  disabled={!file}
                  className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-slate-300 text-white font-bold py-3 px-4 rounded-lg shadow-md transition"
                >
                  Start Batch Processing
                </button>
              </div>
            </div>
          )}

          {status === 'UPLOADING' && (
            <div className="text-center py-20 flex flex-col items-center">
              <div className="w-16 h-16 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mb-4"></div>
              <h3 className="text-xl font-bold text-slate-700">Uploading ZIP...</h3>
            </div>
          )}

          {(status === 'PROCESSING' || status === 'COMPLETED' || status === 'FAILED') && (
            <div className="space-y-6">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <div className="flex justify-between items-end mb-2">
                  <div>
                    <h4 className="font-bold text-slate-800 text-lg">Pipeline Status: {status}</h4>
                    <p className="text-sm text-slate-500">Processing {progress.total} bidders</p>
                  </div>
                  <div className="text-3xl font-bold text-purple-600">
                    {Math.round((progress.processed / Math.max(1, progress.total)) * 100)}%
                  </div>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-4 overflow-hidden shadow-inner">
                  <div 
                    className="bg-purple-500 h-4 rounded-full transition-all duration-500" 
                    style={{width: `${(progress.processed / Math.max(1, progress.total)) * 100}%`}}>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(bidders).map(([bidderId, bData]) => (
                  <div key={bidderId} className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
                    <div className="flex justify-between items-center mb-3">
                      <span className="font-bold text-slate-700">{bidderId}</span>
                      <span className={`text-xs px-2 py-1 rounded font-bold ${
                        bData.status === 'COMPLETED' ? 'bg-green-100 text-green-700' :
                        bData.status === 'PROCESSING' ? 'bg-blue-100 text-blue-700 animate-pulse' :
                        'bg-slate-100 text-slate-500'
                      }`}>
                        {bData.status}
                      </span>
                    </div>
                    {bData.status === 'COMPLETED' && (
                      <div className="space-y-2 text-sm bg-slate-50 p-3 rounded">
                        <div className="flex justify-between">
                          <span className="text-slate-500">Compliance Score:</span>
                          <span className="font-bold">{bData.compliance_score ?? 'N/A'}/100</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Experience (WO):</span>
                          <span className="font-bold text-emerald-600">₹{bData.experience_result?.eligible_cr ?? 0} Cr</span>
                        </div>
                        <div className="flex justify-between border-t border-slate-200 pt-2 mt-2">
                          <span className="text-slate-500">Risk Assessment:</span>
                          <span className={`font-bold ${
                            bData.risk_level === 'LOW' ? 'text-green-600' :
                            bData.risk_level === 'MEDIUM' ? 'text-yellow-600' :
                            bData.risk_level === 'HIGH' ? 'text-orange-600' :
                            'text-red-600'
                          }`}>
                            {bData.risk_level?.replace(/_/g, ' ')}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
