import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function ExperiencePanel() {
  const { experienceResult } = useDashboardStore();

  if (!experienceResult) return null;

  return (
    <div className="bg-white border rounded-lg overflow-hidden mb-6 shadow-sm">
      <div className="px-4 py-3 bg-gray-50 border-b flex justify-between items-center">
        <h2 className="font-semibold text-gray-800 flex items-center gap-2">
          <span>💼</span> Past Experience Validation
        </h2>
        <div className={`text-xs font-bold px-2 py-1 rounded ${experienceResult.result === 'PASS' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {experienceResult.result}
        </div>
      </div>
      <div className="p-4 text-sm">
        <p className="text-gray-600 mb-4">{experienceResult.note}</p>
        
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-50 p-3 rounded border text-center">
            <div className="text-xs text-gray-500 uppercase">Requirement</div>
            <div className="text-xl font-bold text-gray-800">₹{experienceResult.requirement_cr} Cr</div>
          </div>
          <div className="bg-blue-50 p-3 rounded border border-blue-100 text-center">
            <div className="text-xs text-blue-500 uppercase">Eligible Proven</div>
            <div className="text-xl font-bold text-blue-800">₹{experienceResult.eligible_cr} Cr</div>
          </div>
        </div>

        {experienceResult.evidence?.length > 0 && (
          <div>
            <h3 className="font-semibold text-gray-700 mb-2 text-xs uppercase tracking-wider">Eligible Work Orders</h3>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 text-gray-500 border-y">
                  <th className="py-2 px-2">WO Number</th>
                  <th className="py-2 px-2">Client</th>
                  <th className="py-2 px-2">Date</th>
                  <th className="py-2 px-2 text-right">Value (Cr)</th>
                </tr>
              </thead>
              <tbody>
                {experienceResult.evidence.map((wo, i) => (
                  <tr key={i} className="border-b">
                    <td className="py-2 px-2 font-mono text-xs">{wo.wo_number}</td>
                    <td className="py-2 px-2">{wo.client}</td>
                    <td className="py-2 px-2 text-gray-500">{wo.order_date}</td>
                    <td className="py-2 px-2 text-right font-semibold">₹{wo.value_cr}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
