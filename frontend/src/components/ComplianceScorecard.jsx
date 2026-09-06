import React from 'react';
import { useDashboardStore } from '../store/dashboardStore';

export default function ComplianceScorecard() {
  const { 
    gstParseResult, 
    udyamParseResult, 
    epfoParseResult, 
    verifiedDocResult, 
    experienceResult, 
    technicalMatrixResult 
  } = useDashboardStore();

  if (!verifiedDocResult) return null;

  const contradictionsCount = verifiedDocResult.contradictions?.length || 0;
  
  // Score calculator
  let score = 100;
  if (gstParseResult?.verification?.composition_fail) score -= 30;
  else if (!gstParseResult?.verification?.gstin_found) score -= 15;
  
  if (udyamParseResult && !udyamParseResult.verification?.is_micro) score -= 20;
  
  score -= (contradictionsCount * 20);
  
  if (epfoParseResult?.verification?.contribution_status === 'PENDING') score -= 10;
  else if (epfoParseResult?.verification?.contribution_status === 'MISSING') score -= 15;
  
  if (experienceResult?.result === 'FAIL') score -= 20;
  else if (experienceResult?.result === 'INSUFFICIENT_EVIDENCE') score -= 10;
  
  if (technicalMatrixResult?.overall_result === 'FAIL') score -= 25;
  
  score = Math.max(0, score);
  
  let riskLevel = 'LOW';
  let riskColor = 'text-green-600 bg-green-50 border-green-200';
  
  if (score < 40) {
    riskLevel = 'CRITICAL';
    riskColor = 'text-red-700 bg-red-50 border-red-200';
  } else if (score < 60) {
    riskLevel = 'HIGH';
    riskColor = 'text-orange-700 bg-orange-50 border-orange-200';
  } else if (score < 80) {
    riskLevel = 'MEDIUM';
    riskColor = 'text-yellow-700 bg-yellow-50 border-yellow-200';
  }

  return (
    <div className="bg-white border rounded-lg p-6 shadow-sm mb-6 flex flex-col md:flex-row items-center justify-between">
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-1">Overall Compliance Score</h2>
        <p className="text-sm text-gray-500">Aggregated from document verifications, graphs, and technical parameters</p>
      </div>
      <div className="flex items-center gap-6 mt-4 md:mt-0">
        <div className="flex flex-col items-center">
          <span className="text-4xl font-extrabold text-blue-600">{score}</span>
          <span className="text-xs uppercase font-semibold text-gray-400 tracking-wider">Out of 100</span>
        </div>
        <div className={`px-4 py-2 rounded-md border font-bold ${riskColor}`}>
          {riskLevel} RISK
        </div>
      </div>
    </div>
  );
}
