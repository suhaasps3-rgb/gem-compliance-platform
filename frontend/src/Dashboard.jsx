import React, { useState, useEffect } from 'react';
import EvidenceGraph from './EvidenceGraph';
import ContradictionReview from './ContradictionReview';

import GovDocPanel from './GovDocPanel';
import ComplianceScorecard from './components/ComplianceScorecard';
import ExperiencePanel from './components/ExperiencePanel';
import TechnicalMatrix from './components/TechnicalMatrix';
import TurnoverVerificationCard from './components/TurnoverVerificationCard';

import { useDashboardStore } from './store/dashboardStore';

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
    clearAllDocs(); // Reset all uploaded docs when switching companies
    // If a doc was uploaded, don't re-fetch — use that result instead
    if (verifiedDocResult) return;

    async function fetchData() {
      setLoading(true);
      try {
        await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/verify/bidder/${bidderId}/tender/tender-sih-2026`, { method: 'POST' });
        const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/dashboard/bidder/${bidderId}`);
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
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [bidderId, tenderRules, verifiedDocResult]);

  // Detect document identity mismatch (e.g. Bidder A doc uploaded on Bidder B dashboard)
  useEffect(() => {
    const bidderName = (data?.bidder_details?.name || '').toLowerCase().replace(/\s+private\s+limited|pvt\.?\s*ltd\.?|\s+llc|\s+limited/gi, '').trim();
    const docCompany = (turnoverParseResult?.extracted?.company_name || '').toLowerCase().replace(/\s+private\s+limited|pvt\.?\s*ltd\.?|\s+llc|\s+limited/gi, '').trim();
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

  if (!verifiedDocResult && loading) return <div className="p-12 text-center text-slate-500 font-medium">Assembling Evidence Provenance Graph...</div>;
  if (!verifiedDocResult && error) return <div className="p-12 text-center text-red-500 font-medium">Error: {error}</div>;
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

  return (
    <div className="max-w-5xl mx-auto p-6">

      {/* Uploaded Doc Banner */}
      {verifiedDocResult && (
        <div className="mb-4 flex items-center justify-between bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
          <div className="flex items-center gap-2 text-blue-800 text-sm font-medium">
            <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            Showing results from uploaded document: <span className="font-bold">{verifiedDocResult.bidder_id}</span>
            &nbsp;|&nbsp; Extracted claims: {Object.keys(verifiedDocResult.extracted_claims || {}).join(', ')}
          </div>
          <button
            onClick={clearVerifiedDocResult}
            className="ml-4 text-xs text-blue-600 underline hover:text-blue-800 shrink-0"
          >
            ✕ Clear &amp; return to dropdown
          </button>
        </div>
      )}

      {/* Visual Authenticity Failure Alert Banner */}
      {isVisualAuthFailed && (
        <div className="bg-red-50 border-2 border-red-500 p-5 mb-6 rounded-lg shadow-md flex items-start gap-4 animate-pulse">
          <div className="text-red-600 mt-1">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h3 className="text-red-900 font-extrabold text-lg">CRITICAL COMPLIANCE FAILURE: Missing Signature / Rubber Stamp</h3>
              <span className="text-xs bg-red-600 text-white font-bold px-2.5 py-0.5 rounded-full">PENALTY: -50 PTS</span>
            </div>
            <p className="text-red-800 text-sm mt-1 font-medium">
              The uploaded document failed the Visual Authenticity check. No authorized ink signature, digital signature certificate (DSC token), or official rubber stamp was detected in the execution block. The Overall Compliance Score has been penalized by 50 points and flagged for mandatory officer investigation.
            </p>
          </div>
        </div>
      )}

      {/* Document Identity Mismatch / Score Blocked Banner */}
      {complianceBlockedReason && (
        <div className="bg-red-900 border-2 border-red-700 p-5 mb-6 rounded-lg shadow-xl flex items-start gap-4">
          <div className="text-red-300 mt-1 shrink-0">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/></svg>
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-1">
              <h3 className="text-white font-extrabold text-xl tracking-wide">⛔ COMPLIANCE SCORE BLOCKED</h3>
              <span className="text-xs bg-yellow-400 text-red-900 font-black px-3 py-1 rounded-full animate-pulse">FORGERY ALERT</span>
            </div>
            <p className="text-red-200 text-sm font-semibold mt-1">{complianceBlockedReason}</p>
            <p className="text-red-300 text-xs mt-2">SATARK has detected a potential document substitution attempt. The compliance score cannot be computed until an authentic document matching this bidder's identity is submitted. This event has been logged for audit.</p>
          </div>
        </div>
      )}

      {/* Top Header Panel */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 mb-6 p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Bidder Verification Dashboard</h1>
            <p className="text-slate-500 text-sm mt-1">Target: {displayBidderId}</p>
          </div>
          <div className={`px-4 py-2 rounded-full font-bold text-sm tracking-wide ${
            isVisualAuthFailed || displayData?.overall_status !== 'VERIFIED_COMPLIANT' ? 'bg-red-600 text-white shadow-lg' :
            'bg-emerald-100 text-emerald-800'
          }`}>
            STATUS: {isVisualAuthFailed ? 'CRITICAL — MISSING SIGNATURE / STAMP' : (displayData?.overall_status === 'NON_COMPLIANT' ? 'RED — Mandatory Officer Review / Non-Compliant Evidence' : (displayData?.overall_status?.replace(/_/g, ' ') || 'UNKNOWN'))}
          </div>
        </div>

        <div className="mb-6 bg-slate-50 border border-slate-200 rounded p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
             <div className="flex items-center gap-2 text-slate-700 font-bold text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">1</span>
                AI Interprets
             </div>
             <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path></svg>
             <div className="flex items-center gap-2 text-slate-700 font-bold text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">2</span>
                Deterministic Rules Validate
             </div>
             <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path></svg>
             <div className="flex items-center gap-2 text-slate-700 font-bold text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">3</span>
                Graph Explains
             </div>
             <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path></svg>
             <div className="flex items-center gap-2 text-slate-700 font-bold text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">4</span>
                AI Recommends
             </div>
             <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path></svg>
             <div className="flex items-center gap-2 text-slate-700 font-bold text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">5</span>
                Officer Decides
             </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-8">
          {/* Hard Filters */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Gov Portal Integration Layer (Simulated)</h3>
            <div className="space-y-2">
              {displayData?.hard_filters && Object.entries(displayData.hard_filters).map(([key, val]) => (
                <div key={key} className="flex items-center justify-between bg-slate-50 p-2 rounded border border-slate-100 text-sm">
                  <span className="text-slate-600 capitalize">{key.replace('_', ' ')}</span>
                  <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wider flex items-center gap-1 ${
                      val === 'PASS' ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' :
                      val === 'FAIL' ? 'bg-red-100 text-red-700 border border-red-200' :
                      'bg-orange-100 text-orange-700 border border-orange-200'
                    }`}>
                      {val === 'PASS' ? (
                        <><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg> VERIFIED</>
                      ) : val === 'FAIL' ? (
                        <><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M6 18L18 6M6 6l12 12"></path></svg> FAILED</>
                      ) : (
                        <><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg> UNVERIFIED</>
                      )}
                  </span>
                </div>
              ))}

              {visualAuthResult && (
                <div className="flex items-center justify-between bg-slate-50 p-2 rounded border border-slate-100 text-sm">
                  <span className="text-slate-700 font-semibold">Signature &amp; Stamp Authenticity</span>
                  <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wider flex items-center gap-1 ${
                      visualAuthResult.is_signed_and_stamped ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' :
                      'bg-red-100 text-red-700 border border-red-200'
                    }`}>
                      {visualAuthResult.is_signed_and_stamped ? (
                        <><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg> VERIFIED</>
                      ) : (
                        <><svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M6 18L18 6M6 6l12 12"></path></svg> FAILED (UNSIGNED)</>
                      )}
                  </span>
                </div>
              )}

              {/* Dynamically Extracted Rules */}
              {tenderRules?.length > 0 && (
                <div className="mt-4 pt-4 border-t border-slate-200">
                  <h4 className="text-[10px] font-bold text-blue-500 uppercase tracking-wider mb-2">Tender-Specific Rules (AI Extracted)</h4>
                  {tenderRules.map((rule, idx) => (
                    <div key={idx} className="flex items-center justify-between bg-blue-50 p-2 rounded border border-blue-100 text-sm mb-2">
                      <div className="flex flex-col">
                        <span className="text-blue-800 font-semibold text-xs">{rule.clause}</span>
                        <span className="text-blue-600 text-[10px] truncate max-w-[200px]">{rule.description}</span>
                      </div>
                      <span className="text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wider flex items-center gap-1 bg-emerald-100 text-emerald-700 border border-emerald-200 shrink-0">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg> APPLIED
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
          
          {/* Scores */}
          <div>
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Graph Scoring</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Evidence Confidence</span>
                  <span className="font-semibold text-slate-800">{displayData?.scores?.evidence_confidence || 0} / 1.00</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{width: `${(displayData?.scores?.evidence_confidence || 0) * 100}%`}}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">Probabilistic Risk</span>
                  <span className="font-semibold text-slate-800">{displayData?.scores?.probabilistic_risk || 0} / 100</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                  <div className="bg-amber-500 h-2 rounded-full" style={{width: `${displayData?.scores?.probabilistic_risk || 0}%`}}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        </div>
        <ComplianceScorecard displayData={displayData} bidderDetails={displayData?.bidder_details} />

      {/* ── CA Turnover Verification Card (shown after upload) ── */}
      <TurnoverVerificationCard />

      {/* Missing Mandatory Documents Section */}
      {displayData?.ai_recommendation?.missing_docs?.length > 0 && (
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-6 mb-6">
          <h3 className="text-orange-800 font-bold flex items-center gap-2 text-lg">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            Missing Mandatory Documents
          </h3>
          <p className="text-orange-700 text-sm mt-1 mb-3">The following required documents were not found in the bidder's submission:</p>
          <ul className="list-disc list-inside text-orange-900 text-sm space-y-1 font-medium ml-2">
            {displayData.ai_recommendation.missing_docs.map(doc => (
              <li key={doc}>{doc.replace(/_/g, ' ')}</li>
            ))}
          </ul>
        </div>
      )}

      {/* AI Recommendation Engine */}
      {displayData?.ai_recommendation && (
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 mb-6 overflow-hidden">
          <div className="bg-slate-50 px-6 py-3 border-b border-slate-200 flex justify-between items-center">
            <h2 className="text-slate-800 font-bold flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              AI Recommendation Engine
            </h2>
            <span className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Advisory Only</span>
          </div>
          <div className="p-6">
            <div className="flex items-start gap-6">
              <div className="shrink-0">
                <div className={`px-6 py-3 rounded text-lg font-bold tracking-wider border ${
                  aiDecision === 'RECOMMENDED' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 
                  aiDecision === 'NOT RECOMMENDED' ? 'bg-red-50 text-red-700 border-red-200' :
                  'bg-amber-50 text-amber-700 border-amber-200'
                }`}>
                  {aiDecision}
                </div>
              </div>
              <div className="flex-1">
                <h4 className="text-slate-500 text-sm font-bold uppercase tracking-wider mb-1">AI Reasoning</h4>
                <p className="text-slate-700 text-sm leading-relaxed mb-4">{aiReasoning}</p>
                
                {aiRedFlags.length > 0 && (
                  <>
                    <h4 className="text-slate-500 text-sm font-bold uppercase tracking-wider mb-2">Red Flags</h4>
                    <ul className="space-y-2">
                      {aiRedFlags.map((flag, idx) => (
                        <li key={idx} className="text-red-700 text-sm flex items-start gap-2 bg-red-50 border border-red-100 p-2 rounded">
                          <svg className="w-4 h-4 mt-0.5 shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                          {flag}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Procurement Officer Final Review */}
      <div className={`rounded-lg shadow-sm border mb-6 overflow-hidden ${poDecision ? 'bg-blue-50 border-blue-200' : 'bg-white border-slate-200'}`}>
        <div className={`px-6 py-3 border-b flex justify-between items-center ${poDecision ? 'bg-blue-100 border-blue-200' : 'bg-slate-50 border-slate-200'}`}>
          <h2 className="text-slate-800 font-bold flex items-center gap-2">
            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            Procurement Officer Final Review
          </h2>
          <span className="text-[10px] text-blue-600 uppercase tracking-widest font-bold">Authoritative Decision</span>
        </div>
        <div className="p-6 flex flex-col items-center">
          {poDecision ? (
            <div className="text-center">
              <div className={`inline-block px-8 py-4 rounded-lg text-2xl font-black uppercase tracking-widest border-2 shadow-lg mb-4 ${
                poDecision === 'Approve' ? 'bg-emerald-100 text-emerald-700 border-emerald-500' :
                poDecision === 'Reject' ? 'bg-red-100 text-red-700 border-red-500' :
                'bg-amber-100 text-amber-700 border-amber-500'
              }`}>
                {poDecision}
              </div>
              <p className="text-slate-500 text-sm">Final decision recorded. This supersedes the AI Recommendation.</p>
              <button onClick={() => setPoDecision(null)} className="mt-4 text-xs text-blue-500 hover:underline">Revoke Decision</button>
            </div>
          ) : (
            <>
              <p className="text-slate-600 text-sm mb-6 text-center max-w-2xl">
                Review the AI Recommendation, Hard Filters, and Document Evidence above. Please render the final authoritative procurement decision for <strong>{displayBidderId}</strong>.
              </p>
              <div className="flex gap-4">
                <button 
                  onClick={() => setPoDecision('Approve')}
                  className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded shadow transition-colors"
                >
                  Approve Bidder
                </button>
                <button 
                  onClick={() => setPoDecision('Request Clarification')}
                  className="px-6 py-2 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded shadow transition-colors"
                >
                  Request Clarification
                </button>
                <button 
                  onClick={() => setPoDecision('Reject')}
                  className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded shadow transition-colors"
                >
                  Reject Bidder
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <GovDocPanel bidderDetails={displayData?.bidder_details} />
        <ExperiencePanel />
        <TechnicalMatrix />


      <EvidenceGraph graphData={displayData?.graph_data || { nodes: [], links: [] }} />
      
      <ContradictionReview 
        contradictions={displayData?.active_contradictions || displayData?.contradictions || []} 
        bidderId={displayBidderId} 
      />
      
    </div>
  );
}
