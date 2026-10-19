import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';
import { CountUp, GrowBar } from '../utils/motion';

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
    visualAuthResult,
    complianceBlockedReason
  } = useDashboardStore();

  // ── Forgery Mismatch Detection ──
  const normalize = (name) => {
    if (!name) return '';
    return name.toLowerCase().replace(/[^a-z0-9]/g, '').replace(/(privatelimited|pvtltd|ltd|limited|llc|corp|corporation|inc|industries|enterprises|solutions|technologies|systems|trade|infra|infrastructure|tech)/g, '');
  };
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
      <div role="alert" className="notice notice-bad !p-5 !gap-4">
        <svg className="w-5 h-5 shrink-0 mt-0.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <div className="flex-1 min-w-0">
          <h2 className="text-[16px] font-medium text-red-900">Compliance score blocked</h2>
          <p className="text-[14px] mt-1">
            One or more uploaded documents belong to a different entity than the selected bidder
            ({bidderDetails?.name}). Scoring is suspended until every document is verified to belong to the correct bidder.
          </p>
          <h3 className="text-[13px] font-medium mt-3 mb-1">Mismatched documents</h3>
          <ul>
            {mismatches.map((doc, i) => (
              <li key={i} className="flex items-center justify-between gap-3 min-h-9 border-t border-red-200 text-[14px]">
                <span>{doc}</span>
                <span className="pill pill-bad">Forgery alert</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="text-right shrink-0">
          <div className="text-[30px] leading-none text-red-700 num">—</div>
          <div className="text-[12px] text-red-800 mt-1">Blocked</div>
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
  let riskDot = '#2e7d32';

  if (score < 40) {
    riskLevel = 'CRITICAL';
    riskDot = '#c4242a';
  } else if (score < 60) {
    riskLevel = 'HIGH';
    riskDot = '#c4242a';
  } else if (score < 80) {
    riskLevel = 'MEDIUM';
    riskDot = '#b45309';
  }
  const riskWord = riskLevel.charAt(0) + riskLevel.slice(1).toLowerCase();

  const evidence = displayData?.scores?.evidence_confidence;
  const risk = displayData?.scores?.probabilistic_risk;
  const hasEvidence = typeof evidence === 'number' || (evidence != null && !Number.isNaN(Number(evidence)));
  const hasRisk = typeof risk === 'number' || (risk != null && !Number.isNaN(Number(risk)));
  const Dash = () => <span className="text-slate-400">—</span>;

  return (
    <section aria-label="Compliance scores" className="@container">
      <div className="grid grid-cols-3 @2xl:grid-cols-[1.25fr_1fr_1fr_1fr] gap-px bg-slate-200 border border-slate-200 rounded-lg overflow-hidden">
        {/* The answer figure leads: the score the officer is deciding on */}
        <div className="bg-sheet px-5 py-4 col-span-3 @2xl:col-span-1">
          <div className="label">Overall compliance score</div>
          {complianceBlockedReason ? (
            <div className="mt-1 flex items-baseline gap-2">
              <span className="text-[36px] leading-none num">0</span>
              <span className="text-[14px] text-slate-500">/ 100</span>
              <span className="pill pill-bad ml-1">Blocked</span>
            </div>
          ) : (
            <div className="mt-1 flex items-baseline gap-2">
              <span className="text-[36px] leading-none num"><CountUp value={score} /></span>
              <span className="text-[14px] text-slate-500">/ 100</span>
            </div>
          )}
          <div className="text-[12px] text-slate-500 mt-2">
            From document checks, the evidence graph and technical parameters
          </div>
        </div>

        <div className="bg-sheet px-5 py-4">
          <div className="label">Risk level</div>
          {complianceBlockedReason ? (
            <div className="mt-1 text-[24px] leading-tight text-slate-400">—</div>
          ) : (
            <div className="mt-1 flex items-center gap-2 text-[24px] leading-tight">
              <span className="w-2 h-2 rounded-full shrink-0" style={{ background: riskDot }} aria-hidden="true" />
              {riskWord}
            </div>
          )}
          <div className="text-[12px] text-slate-500 mt-2">Low 80+, medium 60–79, high 40–59</div>
        </div>

        <div className="bg-sheet px-5 py-4">
          <div className="label">Evidence confidence</div>
          <div className="mt-1 text-[24px] leading-tight num">
            {hasEvidence ? <CountUp value={Number(evidence)} decimals={2} /> : <Dash />}
            <span className="text-[14px] text-slate-500 whitespace-nowrap"> / 1.00</span>
          </div>
          {hasEvidence && (
            <div className="mt-2.5 h-1 rounded-full bg-slate-200" role="img" aria-label={`Evidence confidence ${Number(evidence).toFixed(2)} out of 1.00`}>
              <GrowBar className="h-1 rounded-full bg-data" style={{ width: `${Math.min(100, Math.max(0, Number(evidence) * 100))}%` }} />
            </div>
          )}
        </div>

        <div className="bg-sheet px-5 py-4">
          <div className="label">Probabilistic risk</div>
          <div className="mt-1 text-[24px] leading-tight num">
            {hasRisk ? <CountUp value={Number(risk)} decimals={Number.isInteger(Number(risk)) ? 0 : 1} /> : <Dash />}
            <span className="text-[14px] text-slate-500"> / 100</span>
          </div>
          {hasRisk && (
            <div className="mt-2.5 h-1 rounded-full bg-slate-200" role="img" aria-label={`Probabilistic risk ${Number(risk)} out of 100`}>
              <GrowBar className="h-1 rounded-full bg-slate-500" style={{ width: `${Math.min(100, Math.max(0, Number(risk)))}%` }} />
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
