import mockData from '../data/mock_dataset.json';

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

  return {
    overall_status: bidder.expected_status || 'VERIFIED_COMPLIANT',
    hard_filters: {
      gst_active: bidder.gst_mock?.status === 'ACTIVE' ? 'PASS' : 'FAIL',
      not_debarred: bidder.debarment_mock?.is_debarred_currently ? 'FAIL' : 'PASS',
      local_content: (claims.local_content_pct || 0) >= 50 ? 'PASS' : 'FAIL',
      turnover_min: turnoverCr >= 5.0 ? 'PASS' : 'FAIL'
    },
    scores: {
      evidence_confidence: 0.88,
      probabilistic_risk: bidder.expected_status === 'CRITICAL_CONTRADICTION' ? 85 : 12
    },
    graph_data: {
      nodes: [
        { id: 'bidder', label: bidder.name, type: 'entity' },
        { id: 'pan', label: 'PAN: ' + (claims.pan || 'PAN12345'), type: 'claim' },
        { id: 'gst', label: 'GST: Active Regular', type: 'evidence' }
      ],
      links: [
        { source: 'bidder', target: 'pan', label: 'CLAIMS_PAN' },
        { source: 'bidder', target: 'gst', label: 'HAS_GST' }
      ]
    },
    active_contradictions: bidder.expected_status === 'CRITICAL_CONTRADICTION' ? [
      {
        field: 'Turnover',
        claim_value: turnoverCr + ' Cr',
        evidence_value: '2.5 Cr',
        source: 'MCA21',
        severity: 'HIGH',
        explanation: 'MCA21 reported turnover does not match submitted certificate'
      }
    ] : [],
    ai_recommendation: bidder.expected_status === 'VERIFIED_COMPLIANT'
      ? 'Bidder satisfies all statutory eligibility and technical specifications. Recommended for qualification.'
      : 'Discrepancies identified in statutory documentation. Review required by Procurement Officer.',
    bidder_details: {
      name: bidder.name,
      pan: claims.pan || 'XXXXX1234X'
    },
    experience_result: experienceResult,
    technical_matrix_result: technicalMatrixResult,
    turnover_result: turnoverResult
  };
}
