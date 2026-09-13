import mockData from '../data/mock_dataset.json';

/**
 * Constructs a full multi-column NetworkX-equivalent evidence provenance graph
 * mirroring backend/graph_engine.py with connected edges and pulsing red conflict edges.
 */
export function generateEvidenceGraph(bidder) {
  const claims = bidder.claims || {};
  const bidderId = bidder.id;
  const bidderName = bidder.name || bidderId;
  const pan = claims.pan || (
    bidderId === 'bidder-beta-002' ? 'BETAL1234K' :
    bidderId === 'bidder-gamma-003' ? 'BKKPA1234F' :
    bidderId === 'bidder-delta-004' ? 'DELTA5678Z' :
    bidderId === 'bidder-epsilon-005' ? 'EPSILON123' :
    bidderId === 'bidder-zeta-006' ? 'ZETATRD999' :
    bidderId === 'bidder-theta-007' ? 'THETA4444X' :
    'PAN' + bidderId.slice(-4).toUpperCase()
  );

  const nodes = [];
  const edges = [];

  // 1. Column 0: Bidder Identity Node
  nodes.push({
    id: bidderId,
    type: 'Bidder',
    label: bidderName,
    source: null
  });

  // 2. Column 1: Identity Anchor Node (PAN)
  const panAnchorId = `Anchor:PAN:${pan}`;
  nodes.push({
    id: panAnchorId,
    type: 'Anchor',
    label: `PAN: ${pan}`,
    source: null
  });
  edges.push({
    source: bidderId,
    target: panAnchorId,
    relation: 'IDENTIFIES_AS',
    color: 'default'
  });

  // 3. Column 3: Statutory Evidence Nodes (Registries)
  nodes.push({
    id: 'Evidence:MCA21',
    type: 'Evidence',
    label: 'MCA21 Registry',
    source: 'MCA21 API 🟡'
  });

  nodes.push({
    id: 'Evidence:Udyam',
    type: 'Evidence',
    label: 'Udyam MSME Portal',
    source: 'Udyam API 🟡'
  });

  if (bidder.gstn_mock || bidder.gst_mock) {
    nodes.push({
      id: 'Evidence:GSTN',
      type: 'Evidence',
      label: 'GSTN Portal',
      source: 'GSTN API 🟢'
    });
    edges.push({
      source: panAnchorId,
      target: 'Evidence:GSTN',
      relation: 'LINKED_TO',
      color: 'default'
    });
  }

  // 4. Column 2: Declared Claim Nodes
  if (claims.turnover_cr != null) {
    const claimVal = claims.turnover_cr;
    const claimNode = `Claim:Turnover:${claimVal}`;
    nodes.push({
      id: claimNode,
      type: 'Claim',
      label: `Turnover: ₹${claimVal} Cr`,
      source: null
    });
    edges.push({
      source: bidderId,
      target: claimNode,
      relation: 'MAKES_CLAIM',
      color: 'default'
    });
    edges.push({
      source: claimNode,
      target: 'Evidence:MCA21',
      relation: 'VERIFIED_AGAINST',
      color: 'default'
    });
    edges.push({
      source: claimNode,
      target: 'Evidence:Udyam',
      relation: 'VERIFIED_AGAINST',
      color: 'default'
    });
  }

  if (claims.enterprise_type != null) {
    const etype = claims.enterprise_type;
    const claimNode = `Claim:EnterpriseType:${etype}`;
    nodes.push({
      id: claimNode,
      type: 'Claim',
      label: `MSME: ${etype}`,
      source: null
    });
    edges.push({
      source: bidderId,
      target: claimNode,
      relation: 'MAKES_CLAIM',
      color: 'default'
    });
    edges.push({
      source: claimNode,
      target: 'Evidence:Udyam',
      relation: 'VERIFIED_AGAINST',
      color: 'default'
    });
  }

  if (claims.local_content_pct != null) {
    const lc = claims.local_content_pct;
    const claimNode = `Claim:LocalContent:${lc}`;
    nodes.push({
      id: claimNode,
      type: 'Claim',
      label: `Local Content: ${lc}%`,
      source: null
    });
    edges.push({
      source: bidderId,
      target: claimNode,
      relation: 'MAKES_CLAIM',
      color: 'default'
    });
  }

  if (claims.subcontracting_pct != null) {
    const sub = claims.subcontracting_pct;
    const claimNode = `Claim:Subcontracting:${sub}`;
    nodes.push({
      id: claimNode,
      type: 'Claim',
      label: `Subcontracting: ${sub}%`,
      source: null
    });
    edges.push({
      source: bidderId,
      target: claimNode,
      relation: 'MAKES_CLAIM',
      color: 'default'
    });
  }

  // 5. Inconsistencies & Pulsing Neon-Red Conflict Edges (color: 'red')

  // Case A: Beta LLC & High Turnover — MSME Cap Exceeded (Tender Cap <= 15 Cr, Beta = 18 Cr)
  if (claims.turnover_cr != null && claims.turnover_cr > 15) {
    const nodeMSME = 'Evidence:TenderMSME';
    if (!nodes.find(n => n.id === nodeMSME)) {
      nodes.push({
        id: nodeMSME,
        type: 'Evidence',
        label: 'Tender MSME Cap (≤₹15 Cr)',
        source: 'Tender Cap (<=15 Cr) 🔴'
      });
    }
    edges.push({
      source: `Claim:Turnover:${claims.turnover_cr}`,
      target: nodeMSME,
      relation: 'EXCEEDS_CAP',
      color: 'red'
    });
  }

  // Case B: Subcontracting Cap Breach (Tender Cap <= 10%, e.g. Beta LLC 15%, Echo 45%, Foxtrot 15%, Juliet 12%, Kilo 18%)
  if (claims.subcontracting_pct != null && claims.subcontracting_pct > 10) {
    const nodeSub = 'Evidence:TenderSubcontract';
    if (!nodes.find(n => n.id === nodeSub)) {
      nodes.push({
        id: nodeSub,
        type: 'Evidence',
        label: 'Tender Subcontract Cap (≤10%)',
        source: 'Tender Subcontract Cap 🔴'
      });
    }
    edges.push({
      source: `Claim:Subcontracting:${claims.subcontracting_pct}`,
      target: nodeSub,
      relation: 'RULE_BREACH',
      color: 'red'
    });
  }

  // Case C: Make In India Mandate Breach (< 60%, e.g. Gamma 40%, Echo 30%, Foxtrot 35%, Kilo 55%)
  if (claims.local_content_pct != null && claims.local_content_pct < 60) {
    const nodeMII = 'Evidence:TenderMII';
    if (!nodes.find(n => n.id === nodeMII)) {
      nodes.push({
        id: nodeMII,
        type: 'Evidence',
        label: 'Make In India Mandate (≥60%)',
        source: 'Tender MII Rule 🔴'
      });
    }
    edges.push({
      source: `Claim:LocalContent:${claims.local_content_pct}`,
      target: nodeMII,
      relation: 'RULE_BREACH',
      color: 'red'
    });
  }

  // Case D: Active Debarment Check (Gamma, Delta, Kilo)
  if (bidder.debarment_mock?.is_debarred_currently || bidder.vigilance_mock?.is_debarred_currently) {
    const nodeDebar = 'Evidence:DebarmentRegistry';
    if (!nodes.find(n => n.id === nodeDebar)) {
      nodes.push({
        id: nodeDebar,
        type: 'Evidence',
        label: 'MoF Debarment Registry',
        source: 'Vigilance DB 🔴'
      });
    }
    edges.push({
      source: panAnchorId,
      target: nodeDebar,
      relation: 'DEBARRED_ENTITY',
      color: 'red'
    });
  }

  // Case E: Historical Debarment on Closing Date (Theta Logistics)
  if (bidderId === 'bidder-theta-007' || (bidder.debarment_mock?.historical_records && bidder.debarment_mock.historical_records.length > 0)) {
    const nodeDebarHist = 'Evidence:Debarment';
    if (!nodes.find(n => n.id === nodeDebarHist)) {
      nodes.push({
        id: nodeDebarHist,
        type: 'Evidence',
        label: 'Historical Debarment',
        source: 'Closing Date Blacklist 🔴'
      });
    }
    edges.push({
      source: panAnchorId,
      target: nodeDebarHist,
      relation: 'TEMPORAL_VIOLATION',
      color: 'red'
    });
  }

  // Case F: Turnover Contradiction vs MCA21 (Delta Solutions: claimed 8.5Cr vs MCA21 14.5Cr)
  if (bidderId === 'bidder-delta-004' || (claims.turnover_cr <= 10 && bidder.mca21_mock?.reported_turnover_cr > 10)) {
    edges.push({
      source: `Claim:Turnover:${claims.turnover_cr}`,
      target: 'Evidence:MCA21',
      relation: 'EVIDENCE_CONFLICT',
      color: 'red'
    });
  }

  // Case G: Cartel / Shared Director Collusion (Epsilon, Zeta)
  if (bidderId === 'bidder-epsilon-005' || bidderId === 'bidder-zeta-006') {
    const nodeCartel = 'Evidence:CartelNetwork';
    if (!nodes.find(n => n.id === nodeCartel)) {
      nodes.push({
        id: nodeCartel,
        type: 'Evidence',
        label: 'Cartel Network Collusion',
        source: 'Shared Director DIN01234567 🔴'
      });
    }
    edges.push({
      source: panAnchorId,
      target: nodeCartel,
      relation: 'SHARED_DIRECTOR_COLLUSION',
      color: 'red'
    });
  }

  // Case H: Document Tampering / Hash Mismatch (Echo Enterprises)
  if (bidderId === 'bidder-echo-005') {
    const nodeForensic = 'Evidence:ForensicAudit';
    if (!nodes.find(n => n.id === nodeForensic)) {
      nodes.push({
        id: nodeForensic,
        type: 'Evidence',
        label: 'Document Forensic Integrity',
        source: 'Digital Hash Mismatch 🔴'
      });
    }
    edges.push({
      source: `Claim:Turnover:${claims.turnover_cr || 12.0}`,
      target: nodeForensic,
      relation: 'TAMPER_ALERT',
      color: 'red'
    });
  }

  return {
    nodes,
    edges,
    links: edges // Dual compatibility
  };
}

/**
 * Generates active contradiction objects matching ContradictionReview.jsx props.
 */
export function generateContradictions(bidder) {
  const claims = bidder.claims || {};
  const contradictions = [];

  // MSME Cap Breach (Beta LLC: 18.0 Cr > 15.0 Cr)
  if (claims.turnover_cr != null && claims.turnover_cr > 15) {
    contradictions.push({
      contradiction_id: `conflict-msme-cap-${bidder.id}`,
      claim: `Annual Turnover: ₹${claims.turnover_cr} Cr`,
      evidence: 'Tender MSME Cap: Maximum ₹15.0 Cr allowed',
      ai_synthesis: `MSME Eligibility Breach: Bidder's declared turnover of ₹${claims.turnover_cr} Cr exceeds the tender-specified MSME cap of ₹15.0 Cr, indicating the entity does not qualify under MSME reservation.`
    });
  }

  // Subcontracting Cap Breach (Beta LLC: 15% > 10%; Echo: 45%; Foxtrot: 15%)
  if (claims.subcontracting_pct != null && claims.subcontracting_pct > 10) {
    contradictions.push({
      contradiction_id: `conflict-subcontract-${bidder.id}`,
      claim: `Sub-contracting: ${claims.subcontracting_pct}%`,
      evidence: 'Tender Rule 5: Capped at 10%',
      ai_synthesis: `Bidder's technical proposal declares ${claims.subcontracting_pct}% sub-contracting, violating the strict 10% maximum limit enforced by the Procurement Officer.`
    });
  }

  // Make in India Mandate Breach (Gamma: 40% < 60%; Echo: 30%; Foxtrot: 35%; Kilo: 55%)
  if (claims.local_content_pct != null && claims.local_content_pct < 60) {
    contradictions.push({
      contradiction_id: `conflict-mii-${bidder.id}`,
      claim: `Local Content: ${claims.local_content_pct}%`,
      evidence: 'Tender Rule 4: Must be >= 60%',
      ai_synthesis: `Bidder declares only ${claims.local_content_pct}% local content, breaching the strict 60% Make In India mandate extracted from the tender document.`
    });
  }

  // Active Debarment in Central Vigilance (Gamma, Delta, Kilo)
  if (bidder.debarment_mock?.is_debarred_currently || bidder.vigilance_mock?.is_debarred_currently) {
    contradictions.push({
      contradiction_id: `conflict-debarment-current-${bidder.id}`,
      claim: 'Vendor Integrity: Eligible Bidder',
      evidence: 'Ministry of Finance Debarment Registry: ACTIVE BLACKLIST',
      ai_synthesis: 'Disqualification Alert: Bidder is actively blacklisted in the Central Vigilance and MoF Debarment Registry.'
    });
  }

  // Historical Debarment Active on Closing Date (Theta)
  if (bidder.id === 'bidder-theta-007' || (bidder.debarment_mock?.historical_records && bidder.debarment_mock.historical_records.length > 0)) {
    contradictions.push({
      contradiction_id: `conflict-debarment-hist-${bidder.id}`,
      claim: 'Current Status: CLEAN (as of Aug 2026)',
      evidence: 'Debarment active on Tender Closing Date (2025-12-01)',
      ai_synthesis: 'Temporal Policy Violation: While the bidder is currently not debarred, they were actively blacklisted during the tender closing window.'
    });
  }

  // Turnover Contradiction vs MCA21 (Delta Solutions)
  if (bidder.id === 'bidder-delta-004' || (claims.turnover_cr <= 10 && bidder.mca21_mock?.reported_turnover_cr > 10)) {
    contradictions.push({
      contradiction_id: `conflict-turnover-mca-${bidder.id}`,
      claim: `Turnover Claim: ₹${claims.turnover_cr} Cr (Micro MSME)`,
      evidence: `MCA21 API 🟡: ₹${bidder.mca21_mock?.reported_turnover_cr || 14.5} Cr`,
      ai_synthesis: `Bidder claims Micro MSME status (< ₹10 Cr limit), but statutory MCA21 filings reflect ₹${bidder.mca21_mock?.reported_turnover_cr || 14.5} Cr, breaching the MSME category threshold.`
    });
  }

  // Cartel & Collusion Indicator (Epsilon, Zeta)
  if (bidder.id === 'bidder-epsilon-005' || bidder.id === 'bidder-zeta-006') {
    contradictions.push({
      contradiction_id: `conflict-cartel-${bidder.id}`,
      claim: 'Independent Bidder Declaration',
      evidence: 'MCA21 Cross-Matching: Shared Director DIN01234567 & Identical Author Metadata',
      ai_synthesis: 'Collusion & Cartel Signal: Bidder shares common directorship and identical electronic PDF author metadata with a competing bidder in this tender.'
    });
  }

  // Digital Tampering / Hash Anomaly (Echo)
  if (bidder.id === 'bidder-echo-005') {
    contradictions.push({
      contradiction_id: `conflict-forensic-${bidder.id}`,
      claim: 'Certified Balance Sheet Uploaded',
      evidence: 'Digital Forensics: Font layer anomaly and signature hash mismatch',
      ai_synthesis: 'Document Provenance Alert: AI forensic engine detected font rasterization inconsistencies and signature timestamp manipulation.'
    });
  }

  return contradictions;
}

export function getClientMockDashboard(bidderId) {
  const bidders = mockData.bidders || [];
  const bidder = bidders.find((b) => b.id === bidderId) || bidders[0];

  const claims = bidder.claims || {};
  const turnoverCr = claims.turnover_cr || 10.0;

  const caNames = {
    'bidder-acme-001': 'CA Ramesh Kumar Iyer',
    'bidder-beta-002': 'CA Suresh Mehta',
    'bidder-gamma-003': 'CA Anjali Desai'
  };
  const udins = {
    'bidder-acme-001': '25123456AABCDE9812',
    'bidder-beta-002': '25654321BBCDEF1234',
    'bidder-gamma-003': '25987654CCDEGH5678'
  };

  const turnoverResult = {
    document_type: 'CA_TURNOVER_CERTIFICATE',
    extracted: {
      company_name: bidder.name,
      financial_year: '2024-25',
      turnover_cr: turnoverCr,
      ca_name: caNames[bidderId] || 'CA Registered Firm',
      udin: udins[bidderId] || '25999999ZZZZZZ9999',
    },
    verification: {
      turnover_extracted: true,
      udin_format_valid: true,
      udin_verification_state: 'UDIN_FORMAT_VALID',
      source: 'MOCK_DATASET'
    },
    source: 'MOCK_DATASET'
  };

  const workOrders = bidder.work_orders || [];
  const totalWoVal = workOrders.reduce((sum, wo) => sum + (wo.value_cr || 0), 0) || 7.35;

  const experienceResult = {
    result: 'PASS',
    requirement_cr: 5.0,
    eligible_cr: totalWoVal,
    shortfall_cr: 0,
    eligible_period: 'FY 2020-21 to FY 2025-26',
    work_orders_submitted: workOrders.length || 3,
    work_orders_eligible: workOrders.length || 3,
    work_orders_excluded: 0,
    evidence: workOrders.map(wo => ({
      wo_number: wo.wo_number,
      value_cr: wo.value_cr,
      client: wo.client,
      order_date: wo.order_date,
      execution_status: 'COMPLETED'
    })),
    note: 'Eligible experience meets the requirement of ₹5.0 Cr.'
  };

  const technicalMatrixResult = {
    overall_result: 'PASS',
    technical_score: 100.0,
    parameters_evaluated: 4,
    pass_count: 4,
    fail_count: 0,
    missing_count: 0,
    matrix: [
      { parameter: 'Pump Capacity', requirement: '>= 500 m³/hr', vendor_value: '520', unit: 'm³/hr', operator: '>=', result: 'PASS' },
      { parameter: 'Pressure', requirement: '>= 20 bar', vendor_value: '22', unit: 'bar', operator: '>=', result: 'PASS' },
      { parameter: 'Efficiency', requirement: '>= 85 %', vendor_value: '91', unit: '%', operator: '>=', result: 'PASS' },
      { parameter: 'Voltage', requirement: '= 415 V', vendor_value: '415', unit: 'V', operator: '=', result: 'PASS' }
    ],
    summary: '4/4 parameters pass technical requirements.'
  };

  const graphData = generateEvidenceGraph(bidder);
  const activeContradictions = generateContradictions(bidder);
  const pan = claims.pan || (
    bidder.id === 'bidder-beta-002' ? 'BETAL1234K' :
    bidder.id === 'bidder-gamma-003' ? 'BKKPA1234F' :
    bidder.id === 'bidder-delta-004' ? 'DELTA5678Z' :
    'PAN' + bidder.id.slice(-4).toUpperCase()
  );

  return {
    overall_status: bidder.expected_status || (activeContradictions.length > 0 ? 'NEEDS_REVIEW' : 'VERIFIED_COMPLIANT'),
    hard_filters: {
      gst_active: bidder.gst_mock?.status === 'ACTIVE' ? 'PASS' : 'FAIL',
      not_debarred: bidder.debarment_mock?.is_debarred_currently ? 'FAIL' : 'PASS',
      local_content: (claims.local_content_pct || 0) >= 60 ? 'PASS' : 'FAIL',
      turnover_min: turnoverCr >= 5.0 ? 'PASS' : 'FAIL'
    },
    scores: {
      evidence_confidence: activeContradictions.length > 0 ? 0.62 : 0.94,
      probabilistic_risk: activeContradictions.length > 0 ? 78 : 8
    },
    graph_data: graphData,
    active_contradictions: activeContradictions,
    ai_recommendation: bidder.ai_recommendation || (
      activeContradictions.length === 0
        ? {
            decision: 'RECOMMENDED',
            reasoning: 'Bidder satisfies all statutory eligibility and technical specifications. Recommended for qualification.',
            red_flags: [],
            missing_docs: []
          }
        : {
            decision: 'NEEDS REVIEW',
            reasoning: `Found ${activeContradictions.length} active policy and threshold contradiction(s) requiring officer review.`,
            red_flags: activeContradictions.map(c => c.ai_synthesis),
            missing_docs: []
          }
    ),
    bidder_details: {
      name: bidder.name,
      pan: pan
    },
    experience_result: experienceResult,
    technical_matrix_result: technicalMatrixResult,
    turnover_result: turnoverResult
  };
}

