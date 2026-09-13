import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls, MarkerType } from 'reactflow';
import 'reactflow/dist/style.css';

const NODE_WIDTH = 175;
const NODE_HEIGHT = 70;
const VERTICAL_GAP = 32;

const COL_X = {
  Bidder: 40,
  Anchor: 270,
  Claim: 520,
  Evidence: 790,
  Rule: 1070
};

// Column-based layout: group nodes by semantic type, distribute evenly across columns
function autoLayout(nodes, rawEdges) {
  const conflictNodeIds = new Set();
  (rawEdges || []).forEach(e => {
    if (e.color === 'red') {
      conflictNodeIds.add(e.source);
      conflictNodeIds.add(e.target);
    }
  });

  const columns = {
    Bidder: [],
    Anchor: [],
    Claim: [],
    Evidence: [],
    Rule: []
  };

  nodes.forEach(n => {
    const rawType = (n.type || '').toLowerCase();
    const id = n.id || '';

    if (rawType === 'bidder' || rawType === 'entity') {
      columns.Bidder.push(n);
    } else if (rawType === 'anchor' || id.startsWith('Anchor:')) {
      columns.Anchor.push(n);
    } else if (rawType === 'claim' || id.startsWith('Claim:')) {
      columns.Claim.push(n);
    } else if (
      rawType === 'rule' ||
      id.includes('Tender') ||
      id.includes('Debarment') ||
      id.includes('Cap') ||
      id.includes('Cartel') ||
      id.includes('Forensic') ||
      (rawType === 'evidence' && conflictNodeIds.has(id))
    ) {
      columns.Rule.push(n);
    } else {
      columns.Evidence.push(n);
    }
  });

  const positioned = [];
  const CANVAS_CENTER_Y = 175;

  for (const [colName, colNodes] of Object.entries(columns)) {
    const count = colNodes.length;
    if (count === 0) continue;
    const totalH = count * NODE_HEIGHT + (count - 1) * VERTICAL_GAP;
    const startY = CANVAS_CENTER_Y - totalH / 2;
    colNodes.forEach((n, i) => {
      positioned.push({
        ...n,
        x: COL_X[colName] ?? 500,
        y: Math.round(startY + i * (NODE_HEIGHT + VERTICAL_GAP))
      });
    });
  }

  return positioned;
}

const nodeStyle = (type, isConflict) => {
  const normType = (type || '').toLowerCase();

  if (normType === 'bidder' || normType === 'entity') {
    return {
      width: NODE_WIDTH,
      minHeight: NODE_HEIGHT,
      borderRadius: 10,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '8px 10px',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
      color: '#ffffff',
      border: '2px solid #3b82f6',
      boxShadow: '0 4px 12px rgba(15, 23, 42, 0.25)',
      cursor: 'default',
    };
  }

  if (normType === 'anchor') {
    return {
      width: NODE_WIDTH,
      minHeight: NODE_HEIGHT,
      borderRadius: 10,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '8px 10px',
      background: isConflict ? '#fef2f2' : '#fdf4ff',
      color: isConflict ? '#991b1b' : '#7e22ce',
      border: isConflict ? '2px solid #ef4444' : '1.5px solid #d8b4fe',
      boxShadow: isConflict ? '0 0 12px rgba(239, 68, 68, 0.35)' : '0 2px 6px rgba(147, 51, 234, 0.1)',
      cursor: 'default',
    };
  }

  if (normType === 'claim') {
    return {
      width: NODE_WIDTH,
      minHeight: NODE_HEIGHT,
      borderRadius: 10,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '8px 10px',
      background: isConflict ? '#fef2f2' : '#eff6ff',
      color: isConflict ? '#b91c1c' : '#1d4ed8',
      border: isConflict ? '2.5px solid #ef4444' : '1.5px solid #93c5fd',
      boxShadow: isConflict ? '0 0 14px rgba(239, 68, 68, 0.35)' : '0 2px 6px rgba(59, 130, 246, 0.1)',
      cursor: 'default',
    };
  }

  if (normType === 'evidence' || normType === 'rule') {
    if (isConflict) {
      return {
        width: NODE_WIDTH,
        minHeight: NODE_HEIGHT,
        borderRadius: 10,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '8px 10px',
        background: '#fff1f2',
        color: '#991b1b',
        border: '2.5px solid #f43f5e',
        boxShadow: '0 0 14px rgba(244, 63, 94, 0.35)',
        cursor: 'default',
      };
    }
    return {
      width: NODE_WIDTH,
      minHeight: NODE_HEIGHT,
      borderRadius: 10,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '8px 10px',
      background: '#ecfdf5',
      color: '#065f46',
      border: '2px solid #6ee7b7',
      boxShadow: '0 2px 6px rgba(16, 185, 129, 0.1)',
      cursor: 'default',
    };
  }

  return {
    width: NODE_WIDTH,
    minHeight: NODE_HEIGHT,
    borderRadius: 10,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '8px 10px',
    background: '#ffffff',
    color: '#334155',
    border: '1px solid #cbd5e1',
    boxShadow: '0 2px 6px rgba(0, 0, 0, 0.08)',
    cursor: 'default',
  };
};

export default function EvidenceGraph({ graphData }) {
  if (!graphData || !graphData.nodes?.length) return null;

  const rawEdges = graphData.edges || graphData.links || [];

  // Find all node IDs involved in a conflict (both source and target of red edges)
  const conflictNodeIds = useMemo(() => {
    const set = new Set();
    rawEdges.forEach(e => {
      if (e.color === 'red') {
        set.add(e.source);
        set.add(e.target);
      }
    });
    return set;
  }, [rawEdges]);

  const redEdgesCount = useMemo(() => {
    return rawEdges.filter(e => e.color === 'red').length;
  }, [rawEdges]);

  const { rfNodes, rfEdges } = useMemo(() => {
    const laid = autoLayout(graphData.nodes, rawEdges);

    const rfNodes = laid.map(n => {
      const isConflict = conflictNodeIds.has(n.id);
      return {
        id: n.id,
        position: { x: n.x, y: n.y },
        draggable: true,
        data: {
          label: (
            <div style={{ textAlign: 'center', width: '100%' }}>
              <div style={{
                fontSize: 9,
                fontWeight: 800,
                textTransform: 'uppercase',
                letterSpacing: 0.8,
                marginBottom: 3,
                color: isConflict ? '#dc2626' : undefined,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 4
              }}>
                {isConflict && <span style={{ animation: 'ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite' }}>⚠️</span>}
                <span>{n.type}</span>
                {isConflict && (
                  <span style={{ background: '#ef4444', color: '#fff', padding: '0.5px 4px', borderRadius: 3, fontSize: 8, fontWeight: 900 }}>
                    CONFLICT
                  </span>
                )}
              </div>
              <div style={{ fontSize: 11, fontWeight: 700, lineHeight: 1.25, wordBreak: 'break-word' }}>
                {n.label || n.id}
              </div>
              {n.source && (
                <div style={{ fontSize: 9, marginTop: 4, fontWeight: 600, opacity: 0.85 }}>{n.source}</div>
              )}
            </div>
          )
        },
        style: nodeStyle(n.type, isConflict),
      };
    });

    const rfEdges = rawEdges.map((e, i) => {
      const isRed = e.color === 'red';
      return {
        id: `e-${i}`,
        source: e.source,
        target: e.target,
        type: 'smoothstep',
        animated: isRed,
        className: isRed ? 'red-error-edge' : '',
        label: isRed ? `⚠️ ${e.relation}` : e.relation,
        labelStyle: {
          fill: isRed ? '#991b1b' : '#475569',
          fontSize: 10,
          fontWeight: 800,
          letterSpacing: 0.5,
        },
        labelBgStyle: {
          fill: isRed ? '#fff1f2' : '#ffffff',
          fillOpacity: 0.98,
          rx: 5,
          stroke: isRed ? '#f87171' : '#cbd5e1',
          strokeWidth: isRed ? 1.5 : 1
        },
        labelBgPadding: [6, 8],
        style: {
          stroke: isRed ? '#ef4444' : '#94a3b8',
          strokeWidth: isRed ? 3.5 : 1.5,
          strokeDasharray: isRed ? '6 3' : undefined,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: isRed ? '#ef4444' : '#94a3b8',
          width: isRed ? 22 : 16,
          height: isRed ? 22 : 16,
        },
      };
    });

    return { rfNodes, rfEdges };
  }, [graphData, rawEdges, conflictNodeIds]);

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm mb-6 overflow-hidden">
      <style>{`
        @keyframes pulseRedLine {
          0%, 100% {
            stroke: #ff1e1e !important;
            stroke-width: 4px !important;
            filter: drop-shadow(0 0 8px rgba(255, 30, 30, 0.95)) drop-shadow(0 0 2px #ff0000) !important;
            opacity: 1;
          }
          50% {
            stroke: #991b1b !important;
            stroke-width: 2.2px !important;
            filter: drop-shadow(0 0 3px rgba(239, 68, 68, 0.4)) !important;
            opacity: 0.4;
          }
        }
        .red-error-edge path,
        .red-error-edge .react-flow__edge-path,
        .red-error-edge path.react-flow__edge-path {
          animation: pulseRedLine 0.9s infinite ease-in-out !important;
          stroke: #ef4444 !important;
        }
      `}</style>
      
      {/* Header Bar with Status & Flow */}
      <div className="flex flex-col gap-2 px-5 py-3 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-700 uppercase tracking-wider">
            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            Interactive Evidence Provenance Graph (NetworkX Engine)
          </div>
          {redEdgesCount > 0 ? (
            <span className="bg-red-100 text-red-700 border border-red-300 px-2.5 py-1 rounded-full text-[11px] font-bold flex items-center gap-1.5 animate-pulse">
              <span className="w-2 h-2 rounded-full bg-red-600"></span>
              {redEdgesCount} Contradiction{redEdgesCount > 1 ? 's' : ''} Detected (Pulsing Red Edges)
            </span>
          ) : (
            <span className="bg-emerald-100 text-emerald-700 border border-emerald-300 px-2.5 py-1 rounded-full text-[11px] font-bold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
              Fully Verified (0 Inconsistencies)
            </span>
          )}
        </div>

        {/* Provenance Flow Badges */}
        <div className="flex items-center gap-1.5 text-[9px] font-bold uppercase tracking-widest text-slate-500 overflow-x-auto py-0.5">
          <span>Flow:</span>
          <span className="bg-slate-900 text-white px-2 py-0.5 rounded">Bidder Entity</span>
          <span>→</span>
          <span className="bg-purple-100 text-purple-700 px-2 py-0.5 rounded">Identity Anchor (PAN)</span>
          <span>→</span>
          <span className="bg-blue-100 text-blue-700 px-2 py-0.5 rounded">Declared Claim</span>
          <span>→</span>
          <span className="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">Statutory Evidence</span>
          <span>→</span>
          <span className="bg-red-100 text-red-700 border border-red-200 px-2 py-0.5 rounded">Tender Cap / Rule Breach</span>
        </div>

        {/* Visual Graph Legend */}
        <div className="flex items-center gap-4 text-[10px] text-slate-600 pt-1 border-t border-slate-200/60 font-medium">
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-sm bg-slate-800 border border-blue-500"></span>
            <span>Bidder</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-sm bg-purple-100 border border-purple-400"></span>
            <span>Anchor</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-sm bg-blue-100 border border-blue-400"></span>
            <span>Claim</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-sm bg-emerald-100 border border-emerald-400"></span>
            <span>Statutory Evidence</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-sm bg-rose-100 border-2 border-red-500"></span>
            <span>Conflict / Rule</span>
          </div>
          <div className="flex items-center gap-1.5 ml-auto">
            <span className="inline-block w-6 h-0.5 bg-slate-400"></span>
            <span>Verified Edge</span>
          </div>
          <div className="flex items-center gap-1.5 font-bold text-red-600">
            <span className="inline-block w-6 h-1 bg-red-500 rounded animate-pulse"></span>
            <span>Blinking Contradiction Edge</span>
          </div>
        </div>
      </div>

      {/* Graph Canvas */}
      <div style={{ height: 420 }}>
        <ReactFlow
          nodes={rfNodes}
          edges={rfEdges}
          fitView
          fitViewOptions={{ padding: 0.18 }}
          minZoom={0.2}
          maxZoom={1.8}
          attributionPosition="bottom-right"
          proOptions={{ hideAttribution: true }}
        >
          <Background color="#cbd5e1" gap={22} size={1.5} />
          <Controls showInteractive={false} style={{ bottom: 12, right: 12, left: 'unset' }} />
        </ReactFlow>
      </div>
    </div>
  );
}

