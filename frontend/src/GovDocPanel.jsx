// GovDocPanel.jsx — shows extracted fields + cross-checks from GST / Udyam uploads
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
          <span className="text-[9px] bg-white border border-slate-200 text-slate-500 px-2 py-0.5 rounded-full font-semibold">PDF OCR</span>
        </div>
        <button onClick={onClear} className="text-[10px] text-slate-400 hover:text-red-500 underline transition-colors">✕ Clear</button>
      </div>
      {children}
    </div>
  );
}

export default function GovDocPanel() {
  const gstResult   = useDashboardStore(s => s.gstParseResult);
  const udyamResult = useDashboardStore(s => s.udyamParseResult);
  const clearGst    = useDashboardStore(s => s.clearGstParseResult);
  const clearUdyam  = useDashboardStore(s => s.clearUdyamParseResult);

  if (!gstResult && !udyamResult) return null;

  return (
    <div className="mb-6">
      <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        Government Document Verification (OCR)
      </h3>

      {/* ── GST Panel ── */}
      {gstResult && (
        <Panel title="GST Registration Certificate" color="blue" icon="🏛️" onClear={clearGst}>
          <Field label="GSTIN"                value={gstResult.extracted?.gstin}
                 status={gstResult.verification?.gstin_valid_format ? 'ok' : 'fail'} />
          <Field label="State Code"           value={gstResult.extracted?.state_code} />
          <Field label="Legal Name"           value={gstResult.extracted?.legal_name}           status="ok" />
          <Field label="Constitution"         value={gstResult.extracted?.constitution} />
          <Field label="Date of Registration" value={gstResult.extracted?.date_of_registration} />
          <Field label="Registration Type"    value={gstResult.extracted?.registration_type}
                 status={gstResult.verification?.composition_fail ? 'fail' :
                         gstResult.verification?.is_regular_taxpayer ? 'ok' : 'warn'} />
          <Field label="Active Status"        value={gstResult.verification?.registration_active ? 'ACTIVE' : 'INACTIVE'}
                 status={gstResult.verification?.registration_active ? 'ok' : 'fail'} />
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
    </div>
  );
}
