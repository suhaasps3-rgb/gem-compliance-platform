import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function TechnicalMatrix() {
  const { technicalMatrixResult } = useDashboardStore();

  if (!technicalMatrixResult) return (
    <section className="card" aria-labelledby="tech-title">
      <div className="card-head">
        <h2 id="tech-title" className="card-title">Technical specifications matrix</h2>
        <span className="pill pill-neutral">Not yet processed</span>
      </div>
      <p className="mx-5 mb-4 px-4 py-2.5 rounded-md border border-dashed border-slate-300 text-[13px] text-slate-500">
        No technical catalogs processed yet. Upload a tech catalog or use batch mode to evaluate parameters.
      </p>
    </section>
  );

  const pass = technicalMatrixResult.overall_result === 'PASS';

  return (
    <section className="card overflow-hidden" aria-labelledby="tech-title">
      <div className="card-head border-b border-slate-100">
        <h2 id="tech-title" className="card-title">Technical specifications matrix</h2>
        <span className={`pill ${pass ? 'pill-ok' : 'pill-bad'} num`}>
          Score {technicalMatrixResult.technical_score}%
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-[13px] text-left">
          <thead>
            <tr className="text-slate-500">
              <th className="h-10 pl-5 pr-3 font-normal">Parameter</th>
              <th className="h-10 pr-3 font-normal">Tender requirement</th>
              <th className="h-10 pr-3 font-normal text-right">Bidder value</th>
              <th className="h-10 pr-3 font-normal text-right">Deviation</th>
              <th className="h-10 pr-5 font-normal text-right">Result</th>
            </tr>
          </thead>
          <tbody>
            {technicalMatrixResult.matrix.map((row, i) => (
              <tr key={i} className="border-t border-slate-100 hover:bg-slate-50">
                <td className="h-11 pl-5 pr-3 text-ink">{row.parameter}</td>
                <td className="h-11 pr-3 text-slate-600">{row.requirement}</td>
                <td className="h-11 pr-3 text-right num text-ink">{row.vendor_value} <span className="text-slate-500">{row.unit}</span></td>
                <td className={`h-11 pr-3 text-right num ${row.deviation ? 'text-red-700' : 'text-slate-400'}`}>
                  {row.deviation ? (row.deviation > 0 ? `+${row.deviation}` : row.deviation) : '—'}
                </td>
                <td className="h-11 pr-5 text-right">
                  <span className={`pill ${row.result === 'PASS' ? 'pill-ok' : 'pill-bad'}`}>
                    {row.result === 'PASS' ? 'Pass' : 'Fail'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="px-5 py-3 text-[12px] text-slate-500 border-t border-slate-100">
        {technicalMatrixResult.summary} Document-based automatic OCR extraction.
      </p>
    </section>
  );
}
