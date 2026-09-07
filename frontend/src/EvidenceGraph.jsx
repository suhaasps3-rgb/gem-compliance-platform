import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls, MarkerType } from 'reactflow';
import 'reactflow/dist/style.css';

const NODE_WIDTH = 160;
const NODE_HEIGHT = 70;
const COL_X = { Bidder: 0, Claim: 250, Anchor: 250, Evidence: 560 };
const COL_GAP = 110;

// Column-based layout: group nodes by type, stack them vertically with gap
function autoLayout(nodes) {
  const columns = { Bidder: [], Claim: [], Anchor: [], Evidence: [] };

  nodes.forEach(n => {
    const col = columns[n.type] ?? columns['Claim'];
    col.push(n);
  });

  const positioned = [];
  for (const [type, col] of Object.entries(columns)) {
    const totalH = col.length * (NODE_HEIGHT + COL_GAP);
    const startY = -totalH / 2 + 200;
    col.forEach((n, i) => {
      positioned.push({ ...n, x: COL_X[type] ?? 400, y: startY + i * (NODE_HEIGHT + COL_GAP) });
    });
  }
  return positioned;
}

const nodeStyle = (type, isConflict) => ({
  width: NODE_WIDTH,
  minHeight: NODE_HEIGHT,
  borderRadius: 10,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '10px 8px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.10)',
  cursor: 'default',
  ...(type === 'Bidder'  ? { background: '#1e293b', color: '#fff',     border: '2px solid #334155' } :
      type === 'Claim'   ? { background: isConflict ? '#fef2f2' : '#eff6ff',
                              color:  isConflict ? '#b91c1c' : '#1d4ed8',
                              border: isConflict ? '2px solid #fca5a5' : '1.5px solid #93c5fd' } :
      type === 'Anchor'  ? { background: '#fdf4ff', color: '#86198f',  border: '1.5px solid #e9d5ff' } :
      type === 'Evidence'? { background: '#ecfdf5', color: '#065f46',  border: '2px solid #6ee7b7' } :
                           { background: '#fff',    color: '#334155',  border: '1px solid #cbd5e1' }),
});

export default function EvidenceGraph({ graphData }) {
  if (!graphData || !graphData.nodes?.length) return null;

  // Find which node IDs are conflict targets (red edges point to them)
  const conflictTargets = new Set((graphData.edges || []).filter(e => e.color === 'red').map(e => e.source));

  const { rfNodes, rfEdges } = useMemo(() => {
    const laid = autoLayout(graphData.nodes);

    const rfNodes = laid.map(n => ({
      id: n.id,
      position: { x: n.x, y: n.y },
      draggable: true,
      data: {
        label: (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 9, opacity: 0.6, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 3 }}>
              {n.type}
            </div>
            <div style={{ fontSize: 12, fontWeight: 700, lineHeight: 1.3 }}>
              {n.label || n.id}
            </div>
            {n.source && (
              <div style={{ fontSize: 10, marginTop: 4, opacity: 0.8 }}>{n.source}</div>
            )}
          </div>
        )
      },
      style: nodeStyle(n.type, conflictTargets.has(n.id)),
    }));

    const rfEdges = (graphData.edges || []).map((e, i) => {
      const isRed = e.color === 'red';
      return {
        id: `e-${i}`,
        source: e.source,
        target: e.target,
        type: 'smoothstep',
        animated: isRed,
        label: e.relation,
        labelStyle: {
          fill: isRed ? '#dc2626' : '#64748b',
          fontSize: 9,
          fontWeight: 700,
        },
        labelBgStyle: { fill: '#ffffff', fillOpacity: 0.9, rx: 4 },
        labelBgPadding: [4, 6],
        style: {
          stroke: isRed ? '#ef4444' : '#94a3b8',
          strokeWidth: isRed ? 2 : 1.5,
          strokeDasharray: isRed ? '6 3' : undefined,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: isRed ? '#ef4444' : '#94a3b8',
          width: 16,
          height: 16,
        },
      };
    });

    return { rfNodes, rfEdges };
  }, [graphData]);

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm mb-6 overflow-hidden">
      
      <div className="flex flex-col gap-2 px-5 py-3 border-b border-slate-100 bg-white">
        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
            <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            Interactive Evidence Provenance Graph
        </div>
        <div className="flex items-center gap-1.5 text-[9px] font-bold uppercase tracking-widest text-slate-500">
           <span>Flow:</span>
           <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">Requirement</span>
           <span>→</span>
           <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">Document</span>
           <span>→</span>
           <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">Claim</span>
           <span>→</span>
           <span className="bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded">Evidence</span>
           <span>→</span>
           <span className="bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded">Rule</span>
           <span>→</span>
           <span className="bg-red-100 text-red-700 px-1.5 py-0.5 rounded">Contradiction</span>
           <span>→</span>
           <span className="bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded">Risk</span>
           <span>→</span>
           <span className="bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded">Recommendation</span>
        </div>
      </div>


      {/* Graph Canvas */}
      <div style={{ height: 340 }}>
        <ReactFlow
          nodes={rfNodes}
          edges={rfEdges}
          fitView
          fitViewOptions={{ padding: 0.25 }}
          minZoom={0.3}
          maxZoom={2}
          attributionPosition="bottom-right"
          proOptions={{ hideAttribution: true }}
        >
          <Background color="#e2e8f0" gap={20} size={1} />
          <Controls showInteractive={false} style={{ bottom: 12, right: 12, left: 'unset' }} />
        </ReactFlow>
      </div>
    </div>
  );
}
