import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function TurnoverVerificationCard() {
  const r = useDashboardStore(s => s.turnoverParseResult);
  if (!r) return null;
  const ext = r.extracted || {};
  const cr = parseFloat(ext.turnover_cr) || 0;
  const cap = 15.0;
  const req = 5.0;
  const ok = cr >= req && cr <= cap;
  return (
    <div style={{border: ok ? '2px solid #6ee7b7' : '2px solid #fca5a5', borderRadius: 8, marginBottom: 24, background: '#fff', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.08)'}}>
      <div style={{padding: '12px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: ok ? '#ecfdf5' : '#fef2f2', borderBottom: ok ? '1px solid #a7f3d0' : '1px solid #fecaca'}}>
        <h2 style={{fontWeight: 700, fontSize: 15, color: '#1e293b', margin: 0}}>CA Turnover Verification</h2>
        <span style={{fontSize: 11, fontWeight: 700, padding: '2px 12px', borderRadius: 999, background: ok ? '#d1fae5' : '#fee2e2', color: ok ? '#065f46' : '#991b1b', border: ok ? '1px solid #6ee7b7' : '1px solid #fca5a5'}}>
          {ok ? 'COMPLIANT' : 'NON-COMPLIANT'}
        </span>
      </div>
      <div style={{padding: 24}}>
        <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 48, marginBottom: 24}}>
          <div style={{textAlign: 'center'}}>
            <div style={{fontSize: 10, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', marginBottom: 4}}>Min. Required</div>
            <div style={{fontSize: 30, fontWeight: 900, color: '#64748b'}}>Rs.{req} Cr</div>
          </div>
          <div style={{textAlign: 'center', padding: '16px 32px', borderRadius: 12, border: ok ? '2px solid #6ee7b7' : '2px solid #fca5a5', background: ok ? '#ecfdf5' : '#fef2f2'}}>
            <div style={{fontSize: 10, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', marginBottom: 4}}>Extracted Turnover</div>
            <div style={{fontSize: 40, fontWeight: 900, color: ok ? '#065f46' : '#991b1b'}}>Rs.{cr} Cr</div>
            <div style={{fontSize: 11, color: '#94a3b8', marginTop: 4}}>{ext.financial_year || 'FY 2024-25'}</div>
          </div>
          <div style={{textAlign: 'center'}}>
            <div style={{fontSize: 10, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', marginBottom: 4}}>MSME Cap</div>
            <div style={{fontSize: 30, fontWeight: 900, color: '#64748b'}}>Rs.{cap} Cr</div>
          </div>
        </div>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 12, padding: 12, borderRadius: 8, border: cr >= req ? '1px solid #a7f3d0' : '1px solid #fca5a5', background: cr >= req ? '#ecfdf5' : '#fef2f2'}}>
            <span style={{fontWeight: 900, fontSize: 13, color: cr >= req ? '#065f46' : '#991b1b'}}>{cr >= req ? 'PASS' : 'FAIL'}</span>
            <div>
              <div style={{fontSize: 11, fontWeight: 700, color: '#334155'}}>Minimum Turnover</div>
              <div style={{fontSize: 11, color: '#64748b'}}>Rs.{cr} Cr vs Rs.{req} Cr required</div>
            </div>
          </div>
          <div style={{display: 'flex', alignItems: 'center', gap: 12, padding: 12, borderRadius: 8, border: cr <= cap ? '1px solid #a7f3d0' : '1px solid #fca5a5', background: cr <= cap ? '#ecfdf5' : '#fef2f2'}}>
            <span style={{fontWeight: 900, fontSize: 13, color: cr <= cap ? '#065f46' : '#991b1b'}}>{cr <= cap ? 'PASS' : 'EXCEEDS'}</span>
            <div>
              <div style={{fontSize: 11, fontWeight: 700, color: '#334155'}}>MSME Cap Check</div>
              <div style={{fontSize: 11, color: '#64748b'}}>Rs.{cr} Cr vs Rs.{cap} Cr cap</div>
            </div>
          </div>
        </div>
        <div style={{display: 'flex', flexWrap: 'wrap', gap: 16, fontSize: 11, color: '#475569', borderTop: '1px solid #f1f5f9', paddingTop: 12}}>
          {ext.company_name && <span><b>Entity:</b> {ext.company_name}</span>}
          {ext.ca_name && <span><b>CA:</b> {ext.ca_name}</span>}
          {ext.udin && <span><b>UDIN:</b> {ext.udin}</span>}
          {ext.financial_year && <span><b>FY:</b> {ext.financial_year}</span>}
        </div>
      </div>
    </div>
  );
}
