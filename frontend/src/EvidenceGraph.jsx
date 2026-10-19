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

// ── Look: flat fills, one hairline, no glow. Colour only says what the node is or that it conflicts. ──
const BASE_NODE = {
  width: NODE_WIDTH,
  minHeight: NODE_HEIGHT,
  borderRadius: 6,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '8px 10px',
  cursor: 'default',
  boxShadow: 'none',
};

const nodeStyle = (type, isConflict) => {
  const normType = (type || '').toLowerCase();

  // A conflict reads the same whatever kind of node it is
  if (isConflict) {
    return { ...BASE_NODE, background: '#fff4f2', color: '#831c1e', border: '1.5px solid #c4242a' };
  }
  if (normType === 'bidder' || normType === 'entity') {
    return { ...BASE_NODE, background: '#ffffff', color: '#0a0a0a', border: '1.5px solid #0a0a0a' };
  }
  if (normType === 'anchor') {
    return { ...BASE_NODE, background: '#f0f2f5', color: '#33363c', border: '1px solid #d0d4da' };
  }
  if (normType === 'claim') {
    return { ...BASE_NODE, background: '#e8f0fb', color: '#123c78', border: '1px solid #9fbbe6' };
  }
  if (normType === 'evidence' || normType === 'rule') {
    return { ...BASE_NODE, background: '#f1faf4', color: '#14501f', border: '1px solid #b4e6c4' };
  }
  return { ...BASE_NODE, background: '#ffffff', color: '#33363c', border: '1px solid #d0d4da' };
};

// The data carries reliability as a trailing coloured emoji ("MCA21 API 🟡"). Show it as a small dot instead.
const RELIABILITY = { '🟢': '#2e7d32', '🟡': '#b45309', '🔴': '#c4242a' };
function splitSource(source) {
  if (!source) return { text: '', dot: null };
  const m = String(source).match(/\s*(🟢|🟡|🔴)\s*$/u);
  return { text: String(source).replace(/\s*(🟢|🟡|🔴)\s*$/u, ''), dot: m ? RELIABILITY[m[1]] : null };
}
const sentence = (s) => {
  const t = String(s ?? '').replace(/_/g, ' ').toLowerCase();
  return t.charAt(0).toUpperCase() + t.slice(1);
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
      const src = splitSource(n.source);
      return {
        id: n.id,
        position: { x: n.x, y: n.y },
        draggable: true,
        data: {
          label: (
            <div style={{ textAlign: 'center', width: '100%' }}>
              <div style={{
                fontSize: 11,
                fontWeight: 400,
                marginBottom: 3,
                opacity: 0.8,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 6
              }}>
                <span>{sentence(n.type)}</span>
                {isConflict && (
                  <span style={{ background: '#ffedea', color: '#831c1e', padding: '1px 5px', borderRadius: 4, fontSize: 11, fontWeight: 500, opacity: 1 }}>
                    Conflict
                  </span>
                )}
              </div>
              <div style={{ fontSize: 12, fontWeight: 500, lineHeight: 1.3, wordBreak: 'break-word' }}>
                {n.label || n.id}
              </div>
              {n.source && (
                <div style={{ fontSize: 11, marginTop: 4, opacity: 0.85, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 5 }}>
                  {src.dot && <span style={{ width: 6, height: 6, borderRadius: 999, background: src.dot, display: 'inline-block' }} />}
                  <span>{src.text}</span>
                </div>
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
        className: isRed ? 'red-error-edge' : '',
        label: String(e.relation ?? '').replace(/_/g, ' ').toLowerCase(),
        labelStyle: {
          fill: isRed ? '#831c1e' : '#474b52',
          fontSize: 11,
          fontWeight: 500,
        },
        labelBgStyle: {
          fill: isRed ? '#fff4f2' : '#ffffff',
          fillOpacity: 1,
          rx: 4,
          stroke: isRed ? '#f7cbc6' : '#e3e6ea',
          strokeWidth: 1
        },
        labelBgPadding: [6, 8],
        style: {
          stroke: isRed ? '#c4242a' : '#8a909a',
          strokeWidth: isRed ? 2 : 1.25,
          strokeDasharray: isRed ? '6 4' : undefined,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: isRed ? '#c4242a' : '#8a909a',
          width: 16,
          height: 16,
        },
      };
    });

    return { rfNodes, rfEdges };
  }, [graphData, rawEdges, conflictNodeIds]);

  const swatch = (bg, border) => (
    <span className="inline-block w-3 h-3 rounded-[3px] shrink-0" style={{ background: bg, border: `1px solid ${border}` }} aria-hidden="true" />
  );

  return (
    <section className="card overflow-hidden" aria-labelledby="graph-title">
      <style>{`
        .red-error-edge path,
        .red-error-edge .react-flow__edge-path,
        .red-error-edge path.react-flow__edge-path {
          stroke: #c4242a !important;
        }
      `}</style>

      {/* Header: what this is, and whether anything in it conflicts */}
      <div className="card-head border-b border-slate-100 flex-wrap">
        <div className="min-w-0">
          <h2 id="graph-title" className="card-title">Evidence provenance graph</h2>
          <p className="card-note mt-0.5">
            Reads left to right: bidder, identity anchor (PAN), declared claim, statutory evidence, rule breach. NetworkX engine.
          </p>
        </div>
        {redEdgesCount > 0 ? (
          <span className="pill pill-bad">
            {redEdgesCount} contradiction{redEdgesCount > 1 ? 's' : ''} detected
          </span>
        ) : (
          <span className="pill pill-ok">Fully verified, 0 inconsistencies</span>
        )}
      </div>

      {/* Legend: each swatch is the node or edge it explains */}
      <div className="flex flex-wrap items-center gap-x-5 gap-y-1.5 px-5 py-2.5 text-[12px] text-slate-600 border-b border-slate-100">
        <span className="flex items-center gap-1.5">{swatch('#ffffff', '#0a0a0a')}Bidder</span>
        <span className="flex items-center gap-1.5">{swatch('#f0f2f5', '#d0d4da')}Anchor</span>
        <span className="flex items-center gap-1.5">{swatch('#e8f0fb', '#9fbbe6')}Claim</span>
        <span className="flex items-center gap-1.5">{swatch('#f1faf4', '#b4e6c4')}Statutory evidence</span>
        <span className="flex items-center gap-1.5">{swatch('#fff4f2', '#c4242a')}Conflict or rule breach</span>
        <span className="flex items-center gap-1.5 sm:ml-auto">
          <svg width="24" height="6" aria-hidden="true"><line x1="0" y1="3" x2="24" y2="3" stroke="#8a909a" strokeWidth="1.25" /></svg>
          Verified edge
        </span>
        <span className="flex items-center gap-1.5">
          <svg width="24" height="6" aria-hidden="true"><line x1="0" y1="3" x2="24" y2="3" stroke="#c4242a" strokeWidth="2" strokeDasharray="6 4" /></svg>
          Contradiction edge
        </span>
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
          <Background color="#d0d4da" gap={22} size={1} />
          <Controls showInteractive={false} style={{ bottom: 12, right: 12, left: 'unset' }} />
        </ReactFlow>
      </div>
    </section>
  );
}
