import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function TechnicalMatrix() {
  const { technicalMatrixResult } = useDashboardStore();

  if (!technicalMatrixResult) return null;

  return (
    <div className="bg-white border rounded-lg overflow-hidden mb-6 shadow-sm">
      <div className="px-4 py-3 bg-gray-50 border-b flex justify-between items-center">
        <h2 className="font-semibold text-gray-800 flex items-center gap-2">
          <span>⚙️</span> Technical Specifications Matrix
        </h2>
        <div className={`text-xs font-bold px-2 py-1 rounded ${technicalMatrixResult.overall_result === 'PASS' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          SCORE: {technicalMatrixResult.technical_score}%
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="bg-gray-50 text-gray-600 text-xs uppercase border-b">
            <tr>
              <th className="px-4 py-3">Parameter</th>
              <th className="px-4 py-3">Tender Requirement</th>
              <th className="px-4 py-3">Bidder Value</th>
              <th className="px-4 py-3">Deviation</th>
              <th className="px-4 py-3 text-center">Result</th>
            </tr>
          </thead>
          <tbody>
            {technicalMatrixResult.matrix.map((row, i) => (
              <tr key={i} className="border-b hover:bg-gray-50">
                <td className="px-4 py-3 font-medium text-gray-800">{row.parameter}</td>
                <td className="px-4 py-3 text-gray-600 font-mono text-xs">{row.requirement}</td>
                <td className="px-4 py-3 font-semibold">{row.vendor_value} {row.unit}</td>
                <td className="px-4 py-3 text-red-500 font-mono text-xs">
                  {row.deviation ? (row.deviation > 0 ? `+${row.deviation}` : row.deviation) : '-'}
                </td>
                <td className="px-4 py-3 text-center">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${row.result === 'PASS' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {row.result}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="p-3 bg-gray-50 text-xs text-gray-500 border-t">
        {technicalMatrixResult.summary} Document-based automatic OCR extraction.
      </div>
    </div>
  );
}
