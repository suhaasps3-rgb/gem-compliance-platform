export function calculateComplianceScore(data) {
  const {
    displayData,
    verifiedDocResult,
    gstParseResult,
    udyamParseResult,
    epfoParseResult,
    experienceResult,
    technicalMatrixResult,
    visualAuthResult
  } = data;

  let score = 100;
  
  if (displayData?.overall_status === 'NEEDS_REVIEW') score -= 15;
  if (displayData?.overall_status === 'REJECTED' || displayData?.overall_status === 'NON_COMPLIANT') score -= 50;

  const activeContradictions = displayData?.active_contradictions?.length || 
                               verifiedDocResult?.contradictions?.length || 0;
  score -= (activeContradictions * 20);
  
  if (gstParseResult?.verification?.composition_fail) score -= 30;
  else if (!gstParseResult?.verification?.gstin_found) score -= 15;
  
  if (udyamParseResult && !udyamParseResult.verification?.is_micro) score -= 20;

  if (epfoParseResult?.verification?.contribution_status === 'PENDING') score -= 10;
  else if (epfoParseResult?.verification?.contribution_status === 'MISSING') score -= 15;
  
  if (experienceResult?.result === 'FAIL') score -= 20;
  else if (experienceResult?.result === 'INSUFFICIENT_EVIDENCE') score -= 10;
  
  if (technicalMatrixResult?.overall_result === 'FAIL') score -= 25;

  if (visualAuthResult && visualAuthResult.is_signed_and_stamped === false) {
      score -= 50;
  }
  
  score = Math.max(0, score);
  
  let riskLevel = 'LOW';
  let outcome = 'VERIFIED_COMPLIANT';
  
  if (score < 40) {
    riskLevel = 'CRITICAL';
    outcome = 'DISQUALIFIED';
  } else if (score < 60) {
    riskLevel = 'HIGH';
    outcome = 'NEEDS_REVIEW';
  } else if (score < 80) {
    riskLevel = 'MEDIUM';
    outcome = 'NEEDS_REVIEW';
  } else {
    riskLevel = 'LOW';
    outcome = 'VERIFIED_COMPLIANT';
  }

  return { score, riskLevel, outcome };
}
