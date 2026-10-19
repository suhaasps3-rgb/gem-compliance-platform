import React from 'react';

// Unused placeholder: raw serialized nodes. The live graph is EvidenceGraph.jsx.
export default function EvidenceGraphPlaceholder({ graphData }) {
  if (!graphData || !graphData.nodes) return null;

  return (
    <section className="card">
      <div className="card-head border-b border-slate-100">
        <h3 className="card-title">Evidence provenance graph</h3>
        <span className="card-note">In-memory traversal</span>
      </div>
      <div className="px-5 py-4 flex flex-col gap-4">
        <ol className="flex gap-2 items-center flex-wrap">
          {graphData.nodes.map((node, idx) => (
            <li key={node.id || idx} className="flex items-center gap-2">
              <div className={`px-3 py-2 rounded-md border text-[13px] ${node.type === 'Claim' ? 'border-blue-200 bg-blue-50 text-blue-900' : 'border-slate-200 bg-sheet text-slate-800'}`}>
                <div className="text-[12px] text-slate-500">{node.type}</div>
                <div>{node.label || node.id}</div>
                {node.source && <div className="text-[12px] text-slate-500 mt-0.5">{node.source}</div>}
              </div>
              {idx < graphData.nodes.length - 1 && (
                <svg className="w-4 h-4 text-slate-300 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                </svg>
              )}
            </li>
          ))}
        </ol>
        <p className="text-[12px] text-slate-500">The full force-directed visualization is not implemented here; this shows the raw serialized nodes.</p>
      </div>
    </section>
  );
}
