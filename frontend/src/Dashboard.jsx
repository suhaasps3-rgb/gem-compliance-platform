import React, { useState, useEffect } from 'react';
import EvidenceGraph from './EvidenceGraph';
import ContradictionReview from './ContradictionReview';

import GovDocPanel from './GovDocPanel';
import ComplianceScorecard from './components/ComplianceScorecard';
import ExperiencePanel from './components/ExperiencePanel';
import TechnicalMatrix from './components/TechnicalMatrix';
import TurnoverVerificationCard from './components/TurnoverVerificationCard';

import { useDashboardStore } from './store/dashboardStore';
import { getClientMockDashboard } from './utils/mockFallback';
import { RevealOnMount } from './utils/motion';

// Registry check keys arrive as snake_case ids; show them as readable labels.
const CHECK_ACRONYMS = new Set(['gst', 'gstin', 'pan', 'mca', 'epfo', 'esic', 'msme', 'cin', 'din', 'ca', 'itr', 'mii']);
const checkLabel = (key) => {
  const words = String(key).split('_').filter(Boolean);
  if (!words.length) return String(key);
  const out = words.map((w) => (CHECK_ACRONYMS.has(w.toLowerCase()) ? w.toUpperCase() : w.toLowerCase()));
  out[0] = out[0].charAt(0).toUpperCase() + out[0].slice(1);
  return out.join(' ');
};

export default function Dashboard({ bidderId }) {
  const tenderRules = useDashboardStore(s => s.tenderRules);
  const verifiedDocResult = useDashboardStore(s => s.verifiedDocResult);
  const clearVerifiedDocResult = useDashboardStore(s => s.clearVerifiedDocResult);
  const clearAllDocs = useDashboardStore(s => s.clearAllDocs);
  const visualAuthResult = useDashboardStore(s => s.visualAuthResult);
  const turnoverParseResult = useDashboardStore(s => s.turnoverParseResult);
  const complianceBlockedReason = useDashboardStore(s => s.complianceBlockedReason);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // New PO Decision State
  const [poDecision, setPoDecision] = useState(null);

  useEffect(() => {
    // If a doc was uploaded, don't re-fetch — use that result instead
    if (verifiedDocResult) return;

    async function fetchData() {
      setLoading(true);
      try {
        await fetch(`${import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')}/api/v1/verify/bidder/${bidderId}/tender/tender-sih-2026`, { method: 'POST' });
        const res = await fetch(`${import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')}/api/v1/dashboard/bidder/${bidderId}`);
        if (!res.ok) throw new Error("Failed to fetch dashboard data");
        const json = await res.json();
        setData(json);
        if (json.experience_result) {
          useDashboardStore.getState().setExperienceResult(json.experience_result);
        }
        if (json.technical_matrix_result) {
          useDashboardStore.getState().setTechnicalMatrixResult(json.technical_matrix_result);
        }
        if (json.turnover_result) {
          useDashboardStore.getState().setTurnoverParseResult(json.turnover_result);
        }
      } catch (err) {
        console.warn("API request failed, activating client-side mock fallback:", err.message);
        const fallback = getClientMockDashboard(bidderId);
        setData(fallback);
        if (fallback.experience_result) {
          useDashboardStore.getState().setExperienceResult(fallback.experience_result);
        }
        if (fallback.technical_matrix_result) {
          useDashboardStore.getState().setTechnicalMatrixResult(fallback.technical_matrix_result);
        }
        if (fallback.turnover_result) {
          useDashboardStore.getState().setTurnoverParseResult(fallback.turnover_result);
        }
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [bidderId, tenderRules, verifiedDocResult]);

  // Detect document identity mismatch (e.g. Bidder A doc uploaded on Bidder B dashboard)
  useEffect(() => {
    const normalize = (name) => {
    if (!name) return '';
    return name.toLowerCase().replace(/[^a-z0-9]/g, '').replace(/(privatelimited|pvtltd|ltd|limited|llc|corp|corporation|inc|industries|enterprises|solutions|technologies|systems|trade|infra|infrastructure|tech)/g, '');
  };
    const bidderName = normalize(data?.bidder_details?.name);
    const docCompany = normalize(turnoverParseResult?.extracted?.company_name);
    const isFromApi = turnoverParseResult?.source === 'MOCK_DATASET';
    if (!isFromApi && docCompany && bidderName && !docCompany.includes(bidderName) && !bidderName.includes(docCompany)) {
      useDashboardStore.getState().setComplianceBlockedReason(
        `IDENTITY MISMATCH: Uploaded document belongs to "${turnoverParseResult?.extracted?.company_name}" but this dashboard is for "${data?.bidder_details?.name}". Possible document substitution / forgery attempt.`
      );
    } else {
      useDashboardStore.getState().clearComplianceBlock();
    }
  }, [turnoverParseResult, data]);

  // If a bidder PDF was uploaded, use that result instead of the dropdown data
  const displayData = verifiedDocResult || data;
  const displayBidderId = verifiedDocResult ? verifiedDocResult.bidder_id : bidderId;

  if (!verifiedDocResult && loading) {
    // Same frame as the loaded screen, values as flat grey bars, no layout shift when data lands.
    return (
      <div className="p-4 md:p-6 pt-2 md:pt-3 space-y-3" role="status" aria-live="polite">
        <span className="sr-only">Assembling the evidence provenance graph…</span>
        <div className="space-y-2 pb-1" aria-hidden="true">
          <div className="h-3 w-32 rounded bg-slate-200" />
          <div className="h-6 w-64 rounded bg-slate-200" />
          <div className="h-3 w-48 rounded bg-slate-200" />
        </div>
        <div className="h-[112px] rounded-lg bg-slate-200" aria-hidden="true" />
        <div className="h-[200px] rounded-lg bg-slate-200" aria-hidden="true" />
        <div className="h-[120px] rounded-lg bg-slate-200" aria-hidden="true" />
      </div>
    );
  }
  if (!verifiedDocResult && error) {
    return (
      <div className="p-4 md:p-6">
        <p className="notice notice-bad" role="alert">Couldn't load the verification: {error}</p>
      </div>
    );
  }
  if (!displayData) return null;

  // Dynamically blend visual authenticity results into the AI Engine
  const isVisualAuthFailed = visualAuthResult && !visualAuthResult.is_signed_and_stamped;
  const originalAi = displayData?.ai_recommendation || {};
  
  let rawDecision = isVisualAuthFailed ? 'NOT RECOMMENDED' : (originalAi.decision || 'UNKNOWN');
  let aiDecision = 'UNKNOWN';
  if (rawDecision === 'RECOMMENDED') aiDecision = 'Approve';
  else if (rawDecision === 'NOT RECOMMENDED' || rawDecision === 'REJECT') aiDecision = 'Reject';
  else aiDecision = 'Request Clarification';

  const aiReasoning = isVisualAuthFailed ? 
    `CRITICAL FRAUD ALERT: Uploaded document failed visual authenticity check (Missing Signature/Stamp). ${originalAi.reasoning || ''}` : 
    (originalAi.reasoning || '');
    
  const aiRedFlags = [...(originalAi.red_flags || [])];
  if (isVisualAuthFailed) {
    aiRedFlags.unshift("Visual Authenticity Failure: The uploaded document lacks a mandatory authorized ink signature or digital stamp.");
  }

  // ── Presentation helpers (no change to what is decided, only how it is shown) ──
  const bidderName = displayData?.bidder_details?.name || displayBidderId;
  const overall = displayData?.overall_status;
  const statusTone = isVisualAuthFailed || overall === 'NON_COMPLIANT' || overall === 'REJECTED' ? 'bad'
    : overall === 'VERIFIED_COMPLIANT' ? 'ok' : 'warn';
  const statusText = isVisualAuthFailed
    ? 'Critical: missing signature or stamp'
    : overall === 'NON_COMPLIANT'
      ? 'Red: non-compliant evidence, mandatory officer review'
      : overall === 'VERIFIED_COMPLIANT'
        ? 'Verified compliant'
        : (overall ? overall.replace(/_/g, ' ').toLowerCase().replace(/^./, c => c.toUpperCase()) : 'Unknown');
  const decisionTone = aiDecision === 'Approve' ? 'ok' : aiDecision === 'Reject' ? 'bad' : 'warn';
  const pipeline = ['AI interprets', 'Deterministic rules validate', 'Graph explains', 'AI recommends', 'Officer decides'];

  const AlertIcon = (
    <svg className="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
  );

  const checkPill = (val) => (
    val === 'PASS'
      ? <span className="pill pill-ok">Verified</span>
      : val === 'FAIL'
        ? <span className="pill pill-bad">Failed</span>
        : <span className="pill pill-warn">Unverified</span>
  );

  return (
    <RevealOnMount className="p-4 md:p-6 pt-2 md:pt-3 space-y-3">

      {/* Uploaded Doc Banner */}
      {verifiedDocResult && (
        <div className="notice items-center justify-between flex-wrap">
          <div className="text-[13px] text-slate-700 min-w-0">
            Showing results from the uploaded document <span className="font-medium text-ink">{verifiedDocResult.bidder_id}</span>
            <span className="text-slate-400"> · </span>
            Extracted claims: {Object.keys(verifiedDocResult.extracted_claims || {}).join(', ')}
          </div>
          <button onClick={clearVerifiedDocResult} className="btn shrink-0">
            Clear and return to bidder list
          </button>
        </div>
      )}

      {/* Visual Authenticity Failure Alert */}
      {isVisualAuthFailed && (
        <div role="alert" className="notice notice-bad !p-4">
          {AlertIcon}
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-[15px] font-medium text-red-900">Critical compliance failure: missing signature or rubber stamp</h2>
              <span className="pill pill-bad !bg-red-100">Penalty −50 points</span>
            </div>
            <p className="text-[13px] mt-1">
              The uploaded document failed the visual authenticity check. No authorized ink signature, digital signature
              certificate (DSC token) or official rubber stamp was detected in the execution block. The overall compliance
              score has been reduced by 50 points and the bid is flagged for mandatory officer investigation.
            </p>
          </div>
        </div>
      )}

      {/* Document Identity Mismatch / Score Blocked Banner */}
      {complianceBlockedReason && (
        <div role="alert" className="notice notice-bad !p-4">
          {AlertIcon}
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-[15px] font-medium text-red-900">Compliance score blocked</h2>
              <span className="pill pill-bad !bg-red-100">Forgery alert</span>
            </div>
            <p className="text-[13px] mt-1 font-medium">{complianceBlockedReason}</p>
            <p className="text-[13px] mt-1">
              SATARK has detected a potential document substitution attempt. The compliance score cannot be computed until
              an authentic document matching this bidder's identity is submitted. This event has been logged for audit.
            </p>
          </div>
        </div>
      )}

      {/* Title row: who is being reviewed, and the verdict of the evidence so far */}
      <header className="pt-1">
        <div className="flex flex-wrap items-start justify-between gap-x-4 gap-y-2">
          <div className="min-w-0">
            <p className="text-[13px] text-slate-500">Bidder verification</p>
            <h1 className="text-[24px] font-medium leading-tight mt-0.5 break-words">{bidderName}</h1>
            <p className="text-[13px] text-slate-500 mt-1">
              <span className="font-mono text-[12px] whitespace-nowrap">{displayBidderId}</span> · tender SIH-2026
            </p>
          </div>
          <span className={`pill ${statusTone === 'ok' ? 'pill-ok' : statusTone === 'bad' ? 'pill-bad' : 'pill-warn'} !h-7 !text-[13px] max-w-full !whitespace-normal !leading-tight py-1`}>
            {statusText}
          </span>
        </div>
        <ol aria-label="How the verdict is reached" className="mt-3 flex flex-wrap items-center gap-x-1.5 gap-y-1 text-[12px] text-slate-500">
          {pipeline.map((step, i) => (
            <li key={step} className="flex items-center gap-1.5">
              <span className={i === pipeline.length - 1 ? 'text-ink font-medium' : ''}>{step}</span>
              {i < pipeline.length - 1 && (
                <svg className="w-3 h-3 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" /></svg>
              )}
            </li>
          ))}
        </ol>
      </header>

      {/* The score, and what it is made of */}
      <ComplianceScorecard displayData={displayData} bidderDetails={displayData?.bidder_details} />

      {/* Missing Mandatory Documents */}
      {displayData?.ai_recommendation?.missing_docs?.length > 0 && (
        <section className="notice notice-warn !p-0 !block">
          <div className="px-5 py-3.5">
            <h2 className="text-[15px] font-medium text-amber-800">Missing mandatory documents</h2>
            <p className="text-[13px] mt-0.5">These required documents were not found in the bidder's submission.</p>
          </div>
          <ul className="px-5 pb-2">
            {displayData.ai_recommendation.missing_docs.map(doc => (
              <li key={doc} className="flex items-center gap-2 min-h-9 border-t border-amber-200 text-[14px] text-amber-900">
                {doc.replace(/_/g, ' ')}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* AI Recommendation */}
      {displayData?.ai_recommendation && (
        <section className="card @container" aria-labelledby="ai-rec-title">
          <div className="card-head border-b border-slate-100">
            <h2 id="ai-rec-title" className="card-title">AI recommendation</h2>
            <span className="pill pill-neutral">Advisory only</span>
          </div>
          <div className="px-5 py-4 grid gap-x-8 gap-y-4 @xl:grid-cols-[minmax(0,13rem)_1fr]">
            <div>
              <div className="label">Recommendation</div>
              <div className="mt-1 flex items-center gap-2 text-[24px] leading-tight">
                <span
                  className="w-2 h-2 rounded-full shrink-0"
                  style={{ background: decisionTone === 'ok' ? '#2e7d32' : decisionTone === 'bad' ? '#c4242a' : '#b45309' }}
                  aria-hidden="true"
                />
                {aiDecision}
              </div>
            </div>
            <div className="min-w-0">
              <h3 className="text-[14px] font-medium mb-1">Reasoning</h3>
              <p className="text-[14px] text-slate-700 leading-relaxed max-w-prose">{aiReasoning}</p>

              {aiRedFlags.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-[14px] font-medium mb-1">
                    Red flags <span className="text-slate-500 font-normal num">({aiRedFlags.length})</span>
                  </h3>
                  <ul>
                    {aiRedFlags.map((flag, idx) => (
                      <li key={idx} className="flex items-start gap-3 py-2.5 border-t border-slate-100 text-[14px] text-slate-800">
                        <span className="mt-[7px] w-1.5 h-1.5 rounded-full bg-red-600 shrink-0" aria-hidden="true" />
                        <span>{flag}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </section>
      )}

      {/* Contradictions: the officer's next action when the data disagrees with the bidder */}
      <ContradictionReview 
        contradictions={displayData?.active_contradictions || displayData?.contradictions || []} 
        bidderId={displayBidderId} 
      />

      {/* Procurement Officer Final Review */}
      <section className="card" aria-labelledby="decision-title">
        <div className="card-head border-b border-slate-100">
          <h2 id="decision-title" className="card-title">Officer's final decision</h2>
          <span className="card-note">Authoritative · supersedes the AI recommendation</span>
        </div>
        <div className="px-5 py-4">
          {poDecision ? (
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <div className="label">Decision recorded for {displayBidderId}</div>
                <div className="mt-1 flex items-center gap-2 text-[24px] leading-tight">
                  <span
                    className="w-2 h-2 rounded-full shrink-0"
                    style={{ background: poDecision === 'Approve' ? '#2e7d32' : poDecision === 'Reject' ? '#c4242a' : '#b45309' }}
                    aria-hidden="true"
                  />
                  {poDecision}
                </div>
              </div>
              <button onClick={() => setPoDecision(null)} className="btn">Revoke decision</button>
            </div>
          ) : (
            <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-3">
              <p className="text-[14px] text-slate-700 max-w-md">
                Review the AI recommendation, the registry checks and the document evidence, then record the final
                decision for <span className="font-medium text-ink whitespace-nowrap">{displayBidderId}</span>.
              </p>
              <div className="flex flex-wrap gap-2">
                <button onClick={() => setPoDecision('Approve')} className="btn btn-lg btn-primary">
                  Approve bidder
                </button>
                <button onClick={() => setPoDecision('Request Clarification')} className="btn btn-lg">
                  Request clarification
                </button>
                <button onClick={() => setPoDecision('Reject')} className="btn btn-lg btn-danger">
                  Reject bidder
                </button>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Registry checks: one row per hard filter */}
      <section className="card" aria-labelledby="checks-title">
        <div className="card-head">
          <h2 id="checks-title" className="card-title">Registry checks</h2>
          <span className="card-note">Government portal integration layer (simulated)</span>
        </div>
        <div>
          {displayData?.hard_filters && Object.entries(displayData.hard_filters).map(([key, val]) => (
            <div key={key} className="row">
              <span className="text-[14px] text-slate-800">{checkLabel(key)}</span>
              {checkPill(val)}
            </div>
          ))}

          {visualAuthResult && (
            <div className="row">
              <span className="text-[14px] text-slate-800">Signature and stamp authenticity</span>
              {visualAuthResult.is_signed_and_stamped
                ? <span className="pill pill-ok">Verified</span>
                : <span className="pill pill-bad">Failed (unsigned)</span>}
            </div>
          )}

          {/* Dynamically Extracted Rules */}
          {tenderRules?.length > 0 && (
            <>
              <div className="px-5 pt-3 pb-1 border-t border-slate-100 text-[12px] text-slate-500">
                Tender-specific rules (AI extracted)
              </div>
              {tenderRules.map((rule, idx) => (
                <div key={idx} className="row !min-h-[52px]">
                  <div className="min-w-0">
                    <div className="text-[14px] text-slate-800 truncate">{rule.clause}</div>
                    <div className="text-[12px] text-slate-500 truncate max-w-[28rem]">{rule.description}</div>
                  </div>
                  <span className="pill pill-ok">Applied</span>
                </div>
              ))}
            </>
          )}
        </div>
      </section>

      {/* ── CA Turnover Verification Card (shown after upload) ── */}
      <TurnoverVerificationCard />

      <GovDocPanel bidderDetails={displayData?.bidder_details} />
      <ExperiencePanel />
      <TechnicalMatrix />

      <EvidenceGraph graphData={displayData?.graph_data || { nodes: [], links: [] }} />
      
    </RevealOnMount>
  );
}
