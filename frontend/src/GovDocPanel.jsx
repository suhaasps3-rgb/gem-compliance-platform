// GovDocPanel.jsx — shows extracted fields + cross-checks from OCR uploads
import React from 'react';
import { useDashboardStore } from './store/dashboardStore';

function Field({ label, value, status }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0">
      <span className="text-xs text-slate-500 font-medium">{label}</span>
      <div className="flex items-center gap-2">
        <span className="text-xs font-bold text-slate-800">{value ?? '—'}</span>
        {status === 'ok'   && <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 border border-emerald-200">✓ VERIFIED</span>}
        {status === 'warn' && <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 border border-amber-200">⚠ REVIEW</span>}
        {status === 'fail' && <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-red-100 text-red-700 border border-red-200">✗ MISMATCH</span>}
      </div>
    </div>
  );
}

function Panel({ title, color, icon, onClear, children }) {
  const colors = {
    blue: 'border-blue-200 bg-blue-50',
    green: 'border-emerald-200 bg-emerald-50',
  };
  return (
    <div className={`rounded-xl border-2 ${colors[color]} p-4 mb-4 shadow-sm`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-lg">{icon}</span>
          <span className="text-sm font-bold text-slate-700">{title}</span>
          <span className="text-[9px] bg-white border border-slate-200 text-slate-500 px-2 py-0.5 rounded-full font-semibold">PDF Extracted</span>
        </div>
        <button onClick={onClear} className="text-[10px] text-slate-400 hover:text-red-500 underline transition-colors">✕ Clear</button>
      </div>
      {children}
    </div>
  );
}

export default function GovDocPanel({ bidderDetails }) {
  const gstResult   = useDashboardStore(s => s.gstParseResult);
  const udyamResult = useDashboardStore(s => s.udyamParseResult);
  const epfoResult  = useDashboardStore(s => s.epfoParseResult);
  const esicResult  = useDashboardStore(s => s.esicParseResult);
  const startupResult = useDashboardStore(s => s.startupParseResult);
  const nsicResult  = useDashboardStore(s => s.nsicParseResult);
  const turnoverResult = useDashboardStore(s => s.turnoverParseResult);
  const itrResult = useDashboardStore(s => s.itrParseResult);
  const miiResult = useDashboardStore(s => s.miiParseResult);
  const gstr3bResult = useDashboardStore(s => s.gstr3bParseResult);
  const debarmentResult = useDashboardStore(s => s.debarmentParseResult);
  
  const clearGst    = useDashboardStore(s => s.clearGstParseResult);
  const clearUdyam  = useDashboardStore(s => s.clearUdyamParseResult);
  const clearEpfo   = useDashboardStore(s => s.clearEpfoParseResult);
  const clearEsic   = useDashboardStore(s => s.clearEsicParseResult);
  const clearStartup = useDashboardStore(s => s.clearStartupParseResult);
  const clearNsic   = useDashboardStore(s => s.clearNsicParseResult);
  const clearTurnover = useDashboardStore(s => s.clearTurnoverParseResult);
  const clearItr = useDashboardStore(s => s.clearItrParseResult);
  const clearMii = useDashboardStore(s => s.clearMiiParseResult);
  const clearGstr3b = useDashboardStore(s => s.clearGstr3bParseResult);
  const clearDebarment = useDashboardStore(s => s.clearDebarmentParseResult);

  // -- Mismatch Detection Logic --
  const normalize = (name) => name?.toLowerCase().replace(/ private limited/g, '').replace(/ pvt ltd/g, '').replace(/ ltd/g, '').replace(/ corp/g, '').replace(/ llc/g, '').trim() || '';
  const checkMismatch = (extractedName) => {
    if (!bidderDetails?.name || !extractedName) return false;
    return !normalize(extractedName).includes(normalize(bidderDetails.name)) && !normalize(bidderDetails.name).includes(normalize(extractedName));
  };

  const gstNameMismatch = checkMismatch(gstResult?.extracted?.legal_name);
  const udyamNameMismatch = checkMismatch(udyamResult?.extracted?.enterprise_name);
  const epfoNameMismatch = checkMismatch(epfoResult?.extracted?.employer_name);
  const esicNameMismatch = checkMismatch(esicResult?.extracted?.employer_name);
  const startupNameMismatch = checkMismatch(startupResult?.extracted?.entity_name);
  const nsicNameMismatch = checkMismatch(nsicResult?.extracted?.entity_name);
  const turnoverNameMismatch = checkMismatch(turnoverResult?.extracted?.entity_name);
  
  const itrNameMismatch = checkMismatch(itrResult?.extracted?.name);
  const itrPanMismatch = !!(bidderDetails?.pan && itrResult?.extracted?.pan && itrResult.extracted.pan !== bidderDetails.pan);
  const isItrMismatch = itrNameMismatch || itrPanMismatch;

  const miiNameMismatch = checkMismatch(miiResult?.extracted?.entity_name);
  const isMiiMismatch = miiNameMismatch;
  const gstr3bNameMismatch = checkMismatch(gstr3bResult?.extracted?.entity_name);
  const debarmentNameMismatch = checkMismatch(debarmentResult?.extracted?.entity_name);

  if (!gstResult && !udyamResult && !epfoResult && !esicResult && !startupResult && !nsicResult && !turnoverResult && !itrResult && !miiResult && !gstr3bResult && !debarmentResult) return null;

  return (
    <div className="mb-6">
      <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        Government Document Verification (PDF Parsing / OCR)
      </h3>

      {/* ── GST Panel ── */}
      {gstResult && (
        <Panel title="GST Registration Certificate" color="blue" icon="🏛️" onClear={clearGst}>
          <Field label="GSTIN"                value={gstResult.extracted?.gstin}
                 status={gstResult.verification?.gstin_valid_format ? 'ok' : 'fail'} />
          <Field label="State Code"           value={gstResult.extracted?.state_code} />
          <Field label="Legal Name"           value={gstResult.extracted?.legal_name}           status={gstNameMismatch ? "fail" : "ok"} />
          <Field label="Constitution"         value={gstResult.extracted?.constitution} />
          <Field label="Date of Registration" value={gstResult.extracted?.date_of_registration} />
          <Field label="Registration Type"    value={gstResult.extracted?.registration_type}
                 status={gstResult.verification?.composition_fail ? 'fail' :
                         gstResult.verification?.is_regular_taxpayer ? 'ok' : 'warn'} />
          {gstNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
            <Field label="Active Status"        value={gstResult.verification?.registration_active ? 'ACTIVE' : 'INACTIVE'}
                 status={gstResult.verification?.registration_active ? 'ok' : 'fail'} />
          <Field label="GSTR-3B Filing Status" value={gstResult.extracted?.gstr_filing_status || 'FILED'}
                 status={gstResult.extracted?.pending_returns > 0 ? 'fail' : 'ok'} />
          <Field label="Pending Returns"       value={gstResult.extracted?.pending_returns ?? 0}
                 status={gstResult.extracted?.pending_returns > 0 ? 'fail' : 'ok'} />
          {gstResult.verification?.composition_fail && (
            <div className="mt-2 bg-red-50 border border-red-200 rounded px-3 py-2 text-[10px] text-red-700 font-semibold">
              ✗ COMPOSITION dealers cannot issue GST invoices to Government entities.
              Bidder must hold a <strong>Regular</strong> GST registration for B2G procurement.
            </div>
          )}
          <div className="mt-3 text-[9px] text-slate-400 italic bg-white rounded px-2 py-1 border border-slate-100">
            ℹ️ {gstResult.verification?.note}
          </div>
        </Panel>
      )}

      {/* ── Udyam Panel ── */}
      {udyamResult && (
        <Panel title="Udyam Registration Certificate" color="green" icon="🏭" onClear={clearUdyam}>
          <Field label="Udyam Number"         value={udyamResult.extracted?.udyam_number}
                 status={udyamResult.verification?.udyam_number_found ? 'ok' : 'fail'} />
          <Field label="State"                value={udyamResult.extracted?.state_code} />
          <Field label="Enterprise Name"      value={udyamResult.extracted?.enterprise_name}    status="ok" />
          <Field label="Classification"       value={udyamResult.extracted?.enterprise_classification}
                 status={udyamResult.verification?.is_micro ? 'ok' : 'fail'} />
          <Field label="Qualifies as MSME"    value={udyamResult.verification?.is_msme ? 'YES' : 'NO'}
                 status={udyamResult.verification?.is_msme ? 'ok' : 'fail'} />
          <Field label="Qualifies as MICRO"   value={udyamResult.verification?.is_micro ? 'YES' : 'NO'}
                 status={udyamResult.verification?.is_micro ? 'ok' : 'fail'} />
          <Field label="Major Activity"       value={udyamResult.extracted?.major_activity} />
          <Field label="NIC Code"             value={udyamResult.extracted?.nic_code
            ? `${udyamResult.extracted.nic_code} — ${udyamResult.extracted.nic_description}` : null} />
          <Field label="Date of Registration" value={udyamResult.extracted?.date_of_udyam_registration} />
          {!udyamResult.verification?.is_micro && (
            <div className="mt-2 bg-red-50 border border-red-200 rounded px-3 py-2 text-[10px] text-red-700 font-semibold">
              ✗ Bidder declared as <strong>MICRO</strong> enterprise to claim EMD exemption, but
              Udyam certificate shows <strong>{udyamResult.extracted?.enterprise_classification}</strong>.
              Classification mismatch — EMD exemption may not apply.
            </div>
          )}
          <div className="mt-3 text-[9px] text-slate-400 italic bg-white rounded px-2 py-1 border border-slate-100">
            ℹ️ {udyamResult.verification?.note}
          </div>
        </Panel>
      )}

      {/* ── EPFO Panel ── */}
      {epfoResult && (
        <Panel title="EPFO Statement (ECR)" color="blue" icon="🏦" onClear={clearEpfo}>
          <Field label="Employer Name" value={epfoResult.extracted?.employer_name} status={epfoNameMismatch ? "fail" : "ok"} />
          {epfoNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
            <Field label="Employer Code" value={epfoResult.extracted?.employer_code} status={epfoResult.verification?.employer_code_found ? 'ok' : 'fail'} />
          <Field label="Contribution Period" value={epfoResult.extracted?.contribution_period} />
          <Field label="Employee Count" value={epfoResult.extracted?.employee_count} />
          <Field label="Total Amount" value={`₹ ${epfoResult.extracted?.total_contribution || '0'}`} />
          <Field label="Status" value={epfoResult.verification?.contribution_status} status={epfoResult.verification?.contribution_verified ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── ESIC Panel ── */}
      {esicResult && (
        <Panel title="ESIC Challan" color="green" icon="🏥" onClear={clearEsic}>
          <Field label="Employer Name" value={esicResult.extracted?.employer_name} status={esicNameMismatch ? "fail" : "ok"} />
          {epfoNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
            {esicNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
            <Field label="Employer Code" value={esicResult.extracted?.employer_code} status={esicResult.verification?.employer_code_found ? 'ok' : 'fail'} />
          <Field label="Contribution Period" value={esicResult.extracted?.contribution_period} />
          <Field label="Total Amount" value={`₹ ${esicResult.extracted?.contribution_amount || '0'}`} />
          <Field label="Status" value={esicResult.verification?.contribution_status} status={esicResult.verification?.esic_verified ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── Startup India Panel ── */}
      {startupResult && (
        <Panel title="Startup India Certificate" color="blue" icon="🚀" onClear={clearStartup}>
          <Field label="Entity Name" value={startupResult.extracted?.entity_name} status={startupNameMismatch ? "fail" : "ok"} />
          <Field label="Recognition No" value={startupResult.extracted?.recognition_number} status={startupResult.verification?.recognition_number_found ? 'ok' : 'fail'} />
          <Field label="Recognition Date" value={startupResult.extracted?.recognition_date} />
          <Field label="Valid Till" value={startupResult.extracted?.validity} />
          <Field label="Certificate Status" value={startupResult.extracted?.certificate_status} status={startupResult.verification?.certificate_active ? 'ok' : 'fail'} />
          <Field label="EMD Exemption" value={startupResult.verification?.emd_exemption_supported ? 'ELIGIBLE' : 'NOT ELIGIBLE'} status={startupResult.verification?.emd_exemption_supported ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── NSIC Panel ── */}
      {nsicResult && (
        <Panel title="NSIC Certificate" color="green" icon="🏭" onClear={clearNsic}>
          <Field label="Enterprise Name" value={nsicResult.extracted?.enterprise_name} status="ok" />
          {nsicNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
            <Field label="Certificate No" value={nsicResult.extracted?.certificate_number} status={nsicResult.verification?.certificate_number_found ? 'ok' : 'fail'} />
          <Field label="Category" value={nsicResult.extracted?.category} />
          <Field label="Date of Issue" value={nsicResult.extracted?.issue_date} />
          <Field label="Valid Till" value={nsicResult.extracted?.validity} />
          <Field label="EMD Exemption" value={nsicResult.verification?.emd_exemption_supported ? 'ELIGIBLE' : 'NOT ELIGIBLE'} status={nsicResult.verification?.emd_exemption_supported ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── CA Turnover Panel ── */}
      {turnoverResult && (
        <Panel title="CA Turnover Certificate" color="blue" icon="📊" onClear={clearTurnover}>
          <Field label="Company Name" value={turnoverResult.extracted?.company_name} status="ok" />
          {turnoverNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
            <Field label="Financial Year" value={turnoverResult.extracted?.financial_year} />
          <Field label="Turnover" value={turnoverResult.extracted?.turnover_cr ? `₹ ${turnoverResult.extracted.turnover_cr} Cr` : null} status={turnoverResult.verification?.turnover_extracted ? 'ok' : 'fail'} />
          <Field label="CA Name" value={turnoverResult.extracted?.ca_name} />
          <Field label="UDIN" value={turnoverResult.extracted?.udin} status={turnoverResult.verification?.udin_format_valid ? 'ok' : 'fail'} />
          <Field label="UDIN Verification" value={turnoverResult.verification?.udin_verification_state?.replace(/_/g, ' ')} />
        </Panel>
      )}

      {/* ?? ITR Panel ?? */}
      {itrResult && (
        <Panel title="Income Tax Return (ITR)" color="amber" icon="📄" onClear={clearItr}>
          <Field label="Name" value={itrResult.extracted?.name} status={!itrResult.extracted?.name ? 'fail' : (bidderDetails?.name && !itrResult.extracted.name.toLowerCase().includes(bidderDetails.name.toLowerCase().replace(' private limited', '').replace(' ltd', ''))) ? 'fail' : 'ok'} />
          <Field label="PAN" value={itrResult.extracted?.pan} status={!itrResult.extracted?.pan ? 'fail' : (bidderDetails?.pan && itrResult.extracted.pan !== bidderDetails.pan) ? 'fail' : itrResult.verification?.pan_found ? 'ok' : 'fail'} />
          <Field label="Assessment Year" value={itrResult.extracted?.assessment_year} status={itrResult.verification?.is_valid_itr ? 'ok' : 'warn'} />
          <Field label="Acknowledgement No" value={itrResult.extracted?.acknowledgement_number} status={itrResult.extracted?.acknowledgement_number ? 'ok' : 'warn'} />
          <Field label="Filing Date" value={itrResult.extracted?.filing_date} status={itrResult.extracted?.filing_date ? 'ok' : 'warn'} />
          
          {isItrMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The identity extracted from this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}

          <div className="mt-2 text-[10px] text-amber-700 bg-amber-50 p-2 border border-amber-200 rounded">
            {itrResult.verification?.note}
          </div>
        </Panel>
      )}

      {/* ?? MII Panel ?? */}
      {miiResult && (
        <Panel title="Make In India (MII) Declaration" color="emerald" icon="🇮🇳" onClear={clearMii}>
          <Field label="Entity Name" value={miiResult.extracted?.entity_name} status={!miiResult.extracted?.entity_name ? 'warn' : (bidderDetails?.name && !miiResult.extracted.entity_name.toLowerCase().includes(bidderDetails.name.toLowerCase().replace(' private limited', '').replace(' corp', ''))) ? 'fail' : 'ok'} />
          <Field label="Supplier Class" value={miiResult.extracted?.supplier_class} status={miiResult.verification?.meets_class_I_threshold ? 'ok' : 'warn'} />
          <Field label="Local Content" value={miiResult.extracted?.local_content_pct ? `${miiResult.extracted.local_content_pct}%` : null} status={miiResult.verification?.meets_class_I_threshold ? 'ok' : 'warn'} />
          
          {isMiiMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity declaring local content does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}

          <div className="mt-2 text-[10px] text-emerald-700 bg-emerald-50 p-2 border border-emerald-200 rounded">
            {miiResult.verification?.note}
          </div>
        </Panel>
      )}

      {gstr3bResult && (
        <Panel title="GSTR-3B Return" color="indigo" icon="📄" onClear={clearGstr3b}>
          <Field label="Entity Name" value={gstr3bResult.extracted?.entity_name} status={gstr3bNameMismatch ? 'fail' : 'ok'} />
          <Field label="Filing Status" value={gstr3bResult.extracted?.filing_status} status={gstr3bResult.extracted?.filing_status === 'FILED' ? 'ok' : 'fail'} />
          <Field label="Return Period" value={gstr3bResult.extracted?.return_period} status="ok" />
          <Field label="Tax Payable" value={gstr3bResult.extracted?.tax_payable} />
          <Field label="Tax Paid" value={gstr3bResult.extracted?.tax_paid} status="ok" />
          
          {gstr3bNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
          
          <div className="mt-2 text-[10px] text-indigo-700 bg-indigo-50 p-2 border border-indigo-200 rounded">
            {gstr3bResult.verification?.note}
          </div>
        </Panel>
      )}

      {debarmentResult && (
        <Panel title="Debarment Declaration" color="rose" icon="🚨" onClear={clearDebarment}>
          <Field label="Entity Name" value={debarmentResult.extracted?.entity_name} status={debarmentNameMismatch ? 'fail' : 'ok'} />
          <Field label="Declaration" value={debarmentResult.extracted?.declaration} status="ok" />
          
          {debarmentNameMismatch && (
            <div className="mt-3 text-[11px] font-bold text-red-700 bg-red-50 p-2.5 border-2 border-red-300 rounded shadow-sm flex items-start gap-2">
              <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
              POTENTIAL FORGERY MISMATCH: The entity name in this document does not match the registered profile for {bidderDetails?.name?.toUpperCase() || 'the selected bidder'}.
            </div>
          )}
          
          <div className="mt-2 text-[10px] text-rose-700 bg-rose-50 p-2 border border-rose-200 rounded">
            {debarmentResult.verification?.note}
          </div>
        </Panel>
      )}
    </div>
  );
}
