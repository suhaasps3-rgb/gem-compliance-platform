import React from 'react';

export default function EvidenceGraphPlaceholder({ graphData }) {
  if (!graphData || !graphData.nodes) return null;

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 mb-6">
      <h3 className="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">
        Evidence Provenance Graph (In-Memory Traversal)
      </h3>
      <div className="flex flex-col items-center gap-6">
        {/* Mock representation of graph */}
        <div className="flex gap-4 items-center flex-wrap justify-center">
          {graphData.nodes.map((node, idx) => (
            <React.Fragment key={node.id || idx}>
              <div 
                className={`p-3 rounded-lg border-2 text-sm font-medium shadow-sm transition-transform hover:scale-105
                  ${node.type === 'Claim' ? 'border-blue-300 bg-blue-50 text-blue-700' : 
                    node.type === 'Evidence' ? 'border-emerald-300 bg-emerald-50 text-emerald-700' :
                    node.type === 'Anchor' ? 'border-purple-300 bg-purple-50 text-purple-700' :
                    'border-slate-300 bg-white text-slate-700'}`}
              >
                <div className="text-xs opacity-75 mb-1">{node.type}</div>
                <div>{node.label || node.id}</div>
                {node.source && <div className="text-xs mt-1 font-bold">{node.source}</div>}
              </div>
              
              {/* Draw an arrow to the next node if it exists */}
              {idx < graphData.nodes.length - 1 && (
                <svg className="w-6 h-6 text-slate-300 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                </svg>
              )}
            </React.Fragment>
          ))}
        </div>
        
        <div className="text-xs text-slate-400 bg-white px-3 py-1 rounded-full border border-slate-200">
          * Note: Full NetworkX force-directed visualization to be implemented. Shows raw serialized nodes.
        </div>
      </div>
    </div>
  );
}
