import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function ComplianceScorecard({ displayData, bidderDetails }) {
  const { 
    gstParseResult, 
    udyamParseResult, 
    epfoParseResult, 
    esicParseResult,
    startupParseResult,
    nsicParseResult,
    turnoverParseResult,
    itrParseResult,
    miiParseResult,
    gstr3bParseResult,
    debarmentParseResult,
    verifiedDocResult, 
    experienceResult, 
    technicalMatrixResult,
    visualAuthResult
  } = useDashboardStore();

  // ── Forgery Mismatch Detection ──
  const normalize = (name) => name?.toLowerCase().replace(/ private limited/g, '').replace(/ pvt ltd/g, '').replace(/ ltd/g, '').replace(/ corp/g, '').replace(/ llc/g, '').trim() || '';
  const checkMismatch = (extractedName) => {
    if (!bidderDetails?.name || !extractedName) return false;
    return !normalize(extractedName).includes(normalize(bidderDetails.name)) && !normalize(bidderDetails.name).includes(normalize(extractedName));
  };

  const mismatches = [];
  if (checkMismatch(gstParseResult?.extracted?.legal_name)) mismatches.push('GST Certificate');
  if (checkMismatch(udyamParseResult?.extracted?.enterprise_name)) mismatches.push('Udyam Certificate');
  if (checkMismatch(epfoParseResult?.extracted?.employer_name)) mismatches.push('EPFO Statement');
  if (checkMismatch(esicParseResult?.extracted?.employer_name)) mismatches.push('ESIC Challan');
  if (checkMismatch(startupParseResult?.extracted?.entity_name)) mismatches.push('Startup Certificate');
  if (checkMismatch(nsicParseResult?.extracted?.entity_name)) mismatches.push('NSIC Certificate');
  if (checkMismatch(turnoverParseResult?.extracted?.company_name)) mismatches.push('CA Turnover Certificate');
  if (checkMismatch(itrParseResult?.extracted?.name)) mismatches.push('ITR Return');
  if (checkMismatch(miiParseResult?.extracted?.entity_name)) mismatches.push('MII Declaration');
  if (checkMismatch(gstr3bParseResult?.extracted?.entity_name)) mismatches.push('GSTR-3B Return');
  if (checkMismatch(debarmentParseResult?.extracted?.entity_name)) mismatches.push('Debarment Declaration');

  const hasForgery = mismatches.length > 0;

  // ── If forgery mismatch detected, block the entire score ──
  if (hasForgery) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6 shadow-sm mb-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <svg className="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-bold text-red-800 mb-1">⛔ Compliance Score Blocked</h2>
            <p className="text-sm text-red-700 mb-3">
              One or more uploaded documents belong to a <strong>different entity</strong> than the selected bidder
              (<strong>{bidderDetails?.name?.toUpperCase()}</strong>). Scoring is suspended until all documents are verified to belong to the correct bidder.
            </p>
            <div className="bg-white rounded border border-red-200 p-3">
              <p className="text-xs font-bold text-red-800 uppercase tracking-wider mb-2">Mismatched Documents:</p>
              <ul className="space-y-1">
                {mismatches.map((doc, i) => (
                  <li key={i} className="text-sm text-red-700 flex items-center gap-2">
                    <span className="text-red-500">✗</span>
                    <span className="font-semibold">{doc}</span>
                    <span className="text-[10px] bg-red-100 text-red-600 px-2 py-0.5 rounded-full font-bold border border-red-200">FORGERY ALERT</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-4xl font-extrabold text-red-400 line-through">—</span>
            <span className="text-xs uppercase font-semibold text-red-400 tracking-wider">BLOCKED</span>
          </div>
        </div>
      </div>
    );
  }

  // ── Normal scoring logic ──
  let score = 100;
  
  if (displayData?.overall_status === 'NEEDS_REVIEW') score -= 15;
  if (displayData?.overall_status === 'REJECTED') score -= 50;

  const activeContradictions = displayData?.active_contradictions?.length || verifiedDocResult?.contradictions?.length || 0;
  score -= (activeContradictions * 20);
  if (gstParseResult?.verification?.composition_fail) score -= 30;
  else if (!gstParseResult?.verification?.gstin_found) score -= 15;
  
  if (udyamParseResult && !udyamParseResult.verification?.is_micro) score -= 20;

  if (epfoParseResult?.verification?.contribution_status === 'PENDING') score -= 10;
  else if (epfoParseResult?.verification?.contribution_status === 'MISSING') score -= 15;
  
  if (experienceResult?.result === 'FAIL') score -= 20;
  else if (experienceResult?.result === 'INSUFFICIENT_EVIDENCE') score -= 10;
  
  if (technicalMatrixResult?.overall_result === 'FAIL') score -= 25;

  if (visualAuthResult && !visualAuthResult.is_signed_and_stamped) {
      score -= 50;
  }
  
  score = Math.max(0, score);
  
  let riskLevel = 'LOW';
  let riskColor = 'text-green-600 bg-green-50 border-green-200';
  
  if (score < 40) {
    riskLevel = 'CRITICAL';
    riskColor = 'text-red-700 bg-red-50 border-red-200';
  } else if (score < 60) {
    riskLevel = 'HIGH';
    riskColor = 'text-orange-700 bg-orange-50 border-orange-200';
  } else if (score < 80) {
    riskLevel = 'MEDIUM';
    riskColor = 'text-yellow-700 bg-yellow-50 border-yellow-200';
  }

  return (
    <div className="bg-white border rounded-lg p-6 shadow-sm mb-6 flex flex-col md:flex-row items-center justify-between">
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-1">Overall Compliance Score</h2>
        <p className="text-sm text-gray-500">Aggregated from document verifications, graphs, and technical parameters</p>
      </div>
      <div className="flex items-center gap-6 mt-4 md:mt-0">
        <div className="flex flex-col items-center">
          <span className="text-4xl font-extrabold text-blue-600">{score}</span>
          <span className="text-xs uppercase font-semibold text-gray-400 tracking-wider">Out of 100</span>
        </div>
        <div className={`px-4 py-2 rounded-md border font-bold ${riskColor}`}>
          {riskLevel} RISK
        </div>
      </div>
    </div>
  );
}
