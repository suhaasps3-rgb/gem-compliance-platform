import React from 'react';

export default function EvidenceGraphPlaceholder({ graphData }) {
  if (!graphData || !graphData.nodes) return null;

  const anchors = graphData.nodes.filter(n => n.type === 'Anchor');
  const evidences = graphData.nodes.filter(n => n.type === 'Evidence');
  const claims = graphData.nodes.filter(n => n.type === 'Claim');
  const bidders = graphData.nodes.filter(n => n.type === 'Bidder');

  const NodeCard = ({ node }) => {
    let colorClass = 'border-slate-300 bg-white text-slate-700';
    if (node.type === 'Anchor') colorClass = 'border-purple-500 bg-purple-100 text-purple-900 ring-4 ring-purple-500/20 shadow-lg scale-110';
    else if (node.type === 'Evidence') colorClass = 'border-emerald-400 bg-emerald-50 text-emerald-800 shadow';
    else if (node.type === 'Claim') colorClass = 'border-blue-400 bg-blue-50 text-blue-800 shadow';
    
    return (
      <div className={`p-4 rounded-xl border-2 font-medium transition-transform hover:scale-105 z-10 relative text-center w-48 ${colorClass}`}>
        <div className="text-[10px] font-bold opacity-60 mb-1 uppercase tracking-wider">{node.type}</div>
        <div className="text-sm font-bold">{node.label || node.id}</div>
        {node.source && <div className="text-xs mt-2 font-bold bg-white/50 inline-block px-2 py-0.5 rounded">{node.source}</div>}
      </div>
    );
  };

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 mb-6 overflow-hidden">
      <h3 className="text-sm font-semibold text-slate-500 mb-8 uppercase tracking-wider">
        Evidence Provenance Graph (Deterministic Topology)
      </h3>
      
      <div className="relative flex flex-col items-center gap-12 py-4">
        
        {/* Top: Evidence Nodes */}
        <div className="flex gap-8 justify-center w-full">
          {evidences.map((n, i) => (
            <div key={i} className="flex flex-col items-center">
              <NodeCard node={n} />
              <div className="h-8 w-1 bg-emerald-300 rounded mt-2 animate-pulse"></div>
            </div>
          ))}
        </div>

        {/* Middle: Bidder -> Anchor */}
        <div className="flex items-center gap-8 w-full justify-center">
          {bidders.map((n, i) => (
            <React.Fragment key={i}>
              <NodeCard node={n} />
              <svg className="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
              </svg>
            </React.Fragment>
          ))}
          
          {anchors.map((n, i) => (
            <NodeCard key={i} node={n} />
          ))}
        </div>

        {/* Bottom: Claim Nodes */}
        <div className="flex gap-8 justify-center w-full">
          {claims.map((n, i) => (
            <div key={i} className="flex flex-col items-center">
              <div className="h-8 w-1 bg-blue-300 rounded mb-2"></div>
              <NodeCard node={n} />
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
