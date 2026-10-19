// GovDocPanel.jsx — shows extracted fields + cross-checks from OCR uploads
import React from 'react';
import { useDashboardStore } from './store/dashboardStore';

function Field({ label, value, status }) {
  return (
    <div className="flex items-center justify-between gap-4 min-h-10 py-1.5 border-t border-slate-100 first:border-t-0">
      <span className="text-[13px] text-slate-500">{label}</span>
      <div className="flex items-center gap-2 min-w-0">
        <span className="text-[13px] text-ink text-right break-words min-w-0 num">{value ?? '—'}</span>
        {status === 'ok'   && <span className="pill pill-ok">Verified</span>}
        {status === 'warn' && <span className="pill pill-warn">Review</span>}
        {status === 'fail' && <span className="pill pill-bad">Mismatch</span>}
      </div>
    </div>
  );
}

// `color` and `icon` are accepted for backwards compatibility with older call sites; the look no longer depends on them.
function Panel({ title, onClear, children }) {
  return (
    <section className="card overflow-hidden" aria-label={title}>
      <div className="card-head border-b border-slate-100">
        <div className="flex items-center gap-2 min-w-0">
          <h3 className="card-title truncate">{title}</h3>
          <span className="pill pill-neutral hidden sm:inline-flex">PDF extracted</span>
        </div>
        <button onClick={onClear} className="btn !h-7 !px-2 text-[12px] shrink-0">Clear</button>
      </div>
      <div className="px-5 py-2">{children}</div>
    </section>
  );
}

function Mismatch({ children }) {
  return (
    <p role="alert" className="notice notice-bad my-2 text-[13px]">
      <svg className="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
      <span>{children}</span>
    </p>
  );
}

function Note({ children }) {
  if (!children) return null;
  return <p className="text-[12px] text-slate-500 py-2 border-t border-slate-100">{children}</p>;
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
  const normalize = (name) => {
    if (!name) return '';
    return name.toLowerCase().replace(/[^a-z0-9]/g, '').replace(/(privatelimited|pvtltd|ltd|limited|llc|corp|corporation|inc|industries|enterprises|solutions|technologies|systems|trade|infra|infrastructure|tech)/g, '');
  };
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
    <div className="space-y-3">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 px-1 pb-2">
        <h2 className="text-[16px] font-medium">Government document verification</h2>
        <span className="card-note">Extracted from uploaded PDFs by OCR and cross-checked against the bidder profile</span>
      </div>
      {/* ── GST Panel ── */}
      {gstResult && (
        <Panel title="GST Registration Certificate" onClear={clearGst}>
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
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
          )}
            <Field label="Active Status"        value={gstResult.verification?.registration_active ? 'ACTIVE' : 'INACTIVE'}
                 status={gstResult.verification?.registration_active ? 'ok' : 'fail'} />
          <Field label="GSTR-3B Filing Status" value={gstResult.extracted?.gstr_filing_status || 'FILED'}
                 status={gstResult.extracted?.pending_returns > 0 ? 'fail' : 'ok'} />
          <Field label="Pending Returns"       value={gstResult.extracted?.pending_returns ?? 0}
                 status={gstResult.extracted?.pending_returns > 0 ? 'fail' : 'ok'} />
          {gstResult.verification?.composition_fail && (
            <Mismatch>COMPOSITION dealers cannot issue GST invoices to Government entities.
              Bidder must hold a <strong>Regular</strong> GST registration for B2G procurement.
            </Mismatch>
          )}
          <Note>{gstResult.verification?.note}</Note>
        </Panel>
      )}

      {/* ── Udyam Panel ── */}
      {udyamResult && (
        <Panel title="Udyam Registration Certificate" onClear={clearUdyam}>
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
            <Mismatch>Bidder declared as <strong>MICRO</strong> enterprise to claim EMD exemption, but
              Udyam certificate shows <strong>{udyamResult.extracted?.enterprise_classification}</strong>.
              Classification mismatch — EMD exemption may not apply.
            </Mismatch>
          )}
          <Note>{udyamResult.verification?.note}</Note>
        </Panel>
      )}

      {/* ── EPFO Panel ── */}
      {epfoResult && (
        <Panel title="EPFO Statement (ECR)" onClear={clearEpfo}>
          <Field label="Employer Name" value={epfoResult.extracted?.employer_name} status={epfoNameMismatch ? "fail" : "ok"} />
          {epfoNameMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
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
        <Panel title="ESIC Challan" onClear={clearEsic}>
          <Field label="Employer Name" value={esicResult.extracted?.employer_name} status={esicNameMismatch ? "fail" : "ok"} />
          {epfoNameMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
          )}
            {esicNameMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
          )}
            <Field label="Employer Code" value={esicResult.extracted?.employer_code} status={esicResult.verification?.employer_code_found ? 'ok' : 'fail'} />
          <Field label="Contribution Period" value={esicResult.extracted?.contribution_period} />
          <Field label="Total Amount" value={`₹ ${esicResult.extracted?.contribution_amount || '0'}`} />
          <Field label="Status" value={esicResult.verification?.contribution_status} status={esicResult.verification?.esic_verified ? 'ok' : 'warn'} />
        </Panel>
      )}

      {/* ── Startup India Panel ── */}
      {startupResult && (
        <Panel title="Startup India Certificate" onClear={clearStartup}>
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
        <Panel title="NSIC Certificate" onClear={clearNsic}>
          <Field label="Enterprise Name" value={nsicResult.extracted?.enterprise_name} status="ok" />
          {nsicNameMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
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
        <Panel title="CA Turnover Certificate" onClear={clearTurnover}>
          <Field label="Company Name" value={turnoverResult.extracted?.company_name} status="ok" />
          {turnoverNameMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
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
        <Panel title="Income Tax Return (ITR)" onClear={clearItr}>
          <Field label="Name" value={itrResult.extracted?.name} status={!itrResult.extracted?.name ? 'fail' : (bidderDetails?.name && !itrResult.extracted.name.toLowerCase().includes(bidderDetails.name.toLowerCase().replace(' private limited', '').replace(' ltd', ''))) ? 'fail' : 'ok'} />
          <Field label="PAN" value={itrResult.extracted?.pan} status={!itrResult.extracted?.pan ? 'fail' : (bidderDetails?.pan && itrResult.extracted.pan !== bidderDetails.pan) ? 'fail' : itrResult.verification?.pan_found ? 'ok' : 'fail'} />
          <Field label="Assessment Year" value={itrResult.extracted?.assessment_year} status={itrResult.verification?.is_valid_itr ? 'ok' : 'warn'} />
          <Field label="Acknowledgement No" value={itrResult.extracted?.acknowledgement_number} status={itrResult.extracted?.acknowledgement_number ? 'ok' : 'warn'} />
          <Field label="Filing Date" value={itrResult.extracted?.filing_date} status={itrResult.extracted?.filing_date ? 'ok' : 'warn'} />
          
          {isItrMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The identity extracted from this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
          )}

          <Note>{itrResult.verification?.note}</Note>
        </Panel>
      )}

      {/* ?? MII Panel ?? */}
      {miiResult && (
        <Panel title="Make In India (MII) Declaration" onClear={clearMii}>
          <Field label="Entity Name" value={miiResult.extracted?.entity_name} status={!miiResult.extracted?.entity_name ? 'warn' : (bidderDetails?.name && !miiResult.extracted.entity_name.toLowerCase().includes(bidderDetails.name.toLowerCase().replace(' private limited', '').replace(' corp', ''))) ? 'fail' : 'ok'} />
          <Field label="Supplier Class" value={miiResult.extracted?.supplier_class} status={miiResult.verification?.meets_class_I_threshold ? 'ok' : 'warn'} />
          <Field label="Local Content" value={miiResult.extracted?.local_content_pct ? `${miiResult.extracted.local_content_pct}%` : null} status={miiResult.verification?.meets_class_I_threshold ? 'ok' : 'warn'} />
          
          {isMiiMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity declaring local content does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
          )}

          <Note>{miiResult.verification?.note}</Note>
        </Panel>
      )}

      {gstr3bResult && (
        <Panel title="GSTR-3B Return" onClear={clearGstr3b}>
          <Field label="Entity Name" value={gstr3bResult.extracted?.entity_name} status={gstr3bNameMismatch ? 'fail' : 'ok'} />
          <Field label="Filing Status" value={gstr3bResult.extracted?.filing_status} status={gstr3bResult.extracted?.filing_status === 'FILED' ? 'ok' : 'fail'} />
          <Field label="Return Period" value={gstr3bResult.extracted?.return_period} status="ok" />
          <Field label="Tax Payable" value={gstr3bResult.extracted?.tax_payable} />
          <Field label="Tax Paid" value={gstr3bResult.extracted?.tax_paid} status="ok" />
          
          {gstr3bNameMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
          )}
          
          <Note>{gstr3bResult.verification?.note}</Note>
        </Panel>
      )}

      {debarmentResult && (
        <Panel title="Debarment Declaration" onClear={clearDebarment}>
          <Field label="Entity Name" value={debarmentResult.extracted?.entity_name} status={debarmentNameMismatch ? 'fail' : 'ok'} />
          <Field label="Declaration" value={debarmentResult.extracted?.declaration} status="ok" />
          
          {debarmentNameMismatch && (
            <Mismatch><b className="font-medium">Potential forgery mismatch.</b> The entity name in this document does not match the registered profile for {bidderDetails?.name || 'the selected bidder'}.</Mismatch>
          )}
          
          <Note>{debarmentResult.verification?.note}</Note>
        </Panel>
      )}
    </div>
  );
}
