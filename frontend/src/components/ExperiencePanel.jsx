import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function ExperiencePanel() {
  const { experienceResult } = useDashboardStore();

  if (!experienceResult) return (
    <section className="card" aria-labelledby="exp-title">
      <div className="card-head">
        <h2 id="exp-title" className="card-title">Past experience validation</h2>
        <span className="pill pill-neutral">Not yet processed</span>
      </div>
      <p className="mx-5 mb-4 px-4 py-2.5 rounded-md border border-dashed border-slate-300 text-[13px] text-slate-500">
        No work orders processed yet. Upload work orders or use batch mode to calculate eligibility.
      </p>
    </section>
  );

  const pass = experienceResult.result === 'PASS';

  return (
    <section className="card overflow-hidden" aria-labelledby="exp-title">
      <div className="card-head border-b border-slate-100">
        <h2 id="exp-title" className="card-title">Past experience validation</h2>
        <span className={`pill ${pass ? 'pill-ok' : 'pill-bad'}`}>{pass ? 'Pass' : experienceResult.result}</span>
      </div>
      <div className="px-5 py-4 text-[14px]">
        <p className="text-slate-700 mb-4 max-w-prose">{experienceResult.note}</p>

        <div className="grid grid-cols-2 gap-px bg-slate-200 border border-slate-200 rounded-md overflow-hidden mb-5">
          <div className="bg-sheet px-4 py-3">
            <div className="label">Requirement</div>
            <div className="mt-0.5 text-[24px] leading-tight num font-[700]">₹{experienceResult.requirement_cr}<span className="text-[14px] text-slate-500 font-normal"> Cr</span></div>
          </div>
          <div className="bg-sheet px-4 py-3">
            <div className="label">Eligible, proven</div>
            <div className="mt-0.5 text-[24px] leading-tight num font-[700]">₹{experienceResult.eligible_cr}<span className="text-[14px] text-slate-500 font-normal"> Cr</span></div>
          </div>
        </div>

        {experienceResult.evidence?.length > 0 && (
          <div>
            <h3 className="text-[14px] font-medium mb-1">Eligible work orders</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-[13px]">
                <thead>
                  <tr className="text-slate-500">
                    <th className="h-9 pr-3 font-normal">Work order</th>
                    <th className="h-9 pr-3 font-normal">Client</th>
                    <th className="h-9 pr-3 font-normal">Date</th>
                    <th className="h-9 font-normal num text-right">Value (Cr)</th>
                  </tr>
                </thead>
                <tbody>
                  {experienceResult.evidence.map((wo, i) => (
                    <tr key={i} className="border-t border-slate-100">
                      <td className="h-11 pr-3 font-mono text-[12px] whitespace-nowrap">{wo.wo_number}</td>
                      <td className="h-11 pr-3">{wo.client}</td>
                      <td className="h-11 pr-3 text-slate-500 whitespace-nowrap">{wo.order_date}</td>
                      <td className="h-11 text-right num font-[700]">₹{wo.value_cr}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
