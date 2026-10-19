import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';
import { GrowBar } from '../utils/motion';

export default function TurnoverVerificationCard() {
  const r = useDashboardStore(s => s.turnoverParseResult);
  if (!r) return null;
  const ext = r.extracted || {};
  const cr = parseFloat(ext.turnover_cr) || 0;
  const cap = 15.0;
  const req = 5.0;
  const ok = cr >= req && cr <= cap;

  // One scale for the whole bar so the fill is the true ratio: 0 to a little past the larger of cap and turnover.
  const max = Math.max(cap, cr) * 1.15;
  const pct = (v) => `${Math.min(100, Math.max(0, (v / max) * 100))}%`;

  return (
    <section className="card overflow-hidden" aria-labelledby="turnover-title">
      <div className="card-head border-b border-slate-100">
        <h2 id="turnover-title" className="card-title">CA turnover verification</h2>
        <span className={`pill ${ok ? 'pill-ok' : 'pill-bad'}`}>{ok ? 'Compliant' : 'Non-compliant'}</span>
      </div>

      <div className="px-5 pt-4 pb-2">
        <div className="flex items-baseline gap-2">
          <span className="text-[30px] leading-none num font-[700]">₹{cr} Cr</span>
          <span className="text-[13px] text-slate-500">extracted turnover, {ext.financial_year || 'FY 2024-25'}</span>
        </div>

        {/* Turnover against the corridor the tender allows (minimum to MSME cap) */}
        <div className="relative mt-7 mb-9">
          <div className="relative h-2 rounded-full bg-slate-200" role="img"
               aria-label={`Turnover ${cr} crore, against a minimum of ${req} crore and an MSME cap of ${cap} crore`}>
            <GrowBar className="absolute inset-y-0 left-0 rounded-full bg-data" style={{ width: pct(cr) }} />
          </div>
          {[[req, 'Minimum required', `₹${req} Cr`], [cap, 'MSME cap', `₹${cap} Cr`]].map(([v, name, val]) => (
            <div key={name} className="absolute top-0" style={{ left: pct(v) }}>
              <div className="w-px h-5 -mt-1.5 bg-slate-500" aria-hidden="true" />
              <div className="absolute top-5 -translate-x-1/2 whitespace-nowrap text-center text-[12px] leading-tight">
                <div className="text-slate-500">{name}</div>
                <div className="text-ink num">{val}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="row">
          <div>
            <div className="text-[14px]">Minimum turnover</div>
            <div className="text-[12px] text-slate-500 num">₹{cr} Cr against ₹{req} Cr required</div>
          </div>
          <span className={`pill ${cr >= req ? 'pill-ok' : 'pill-bad'}`}>{cr >= req ? 'Pass' : 'Fail'}</span>
        </div>
        <div className="row">
          <div>
            <div className="text-[14px]">MSME cap check</div>
            <div className="text-[12px] text-slate-500 num">₹{cr} Cr against ₹{cap} Cr cap</div>
          </div>
          <span className={`pill ${cr <= cap ? 'pill-ok' : 'pill-bad'}`}>{cr <= cap ? 'Pass' : 'Exceeds'}</span>
        </div>
      </div>

      {(ext.company_name || ext.ca_name || ext.udin || ext.financial_year) && (
        <dl className="flex flex-wrap gap-x-6 gap-y-1 px-5 py-3 border-t border-slate-100 text-[12px] text-slate-500">
          {ext.company_name && <div className="flex gap-1.5"><dt>Entity</dt><dd className="text-ink">{ext.company_name}</dd></div>}
          {ext.ca_name && <div className="flex gap-1.5"><dt>CA</dt><dd className="text-ink">{ext.ca_name}</dd></div>}
          {ext.udin && <div className="flex gap-1.5"><dt>UDIN</dt><dd className="text-ink font-mono">{ext.udin}</dd></div>}
          {ext.financial_year && <div className="flex gap-1.5"><dt>FY</dt><dd className="text-ink">{ext.financial_year}</dd></div>}
        </dl>
      )}
    </section>
  );
}
