import { create } from 'zustand';

export const useDashboardStore = create((set) => ({
  // Active document in Viewer
  selectedDocument: 'tender',
  setSelectedDocument: (docId) => set({ selectedDocument: docId }),

  // Viewer state
  viewerRef: null,
  setViewerRef: (ref) => set({ viewerRef: ref }),

  // Ledger state
  auditLog: [],
  addAuditEntry: (entry) => set((state) => ({ 
    auditLog: [...state.auditLog, { ...entry, timestamp: new Date().toISOString() }] 
  })),

  // Evaluated tender rules
  tenderRules: null,
  setTenderRules: (rules) => set({ tenderRules: rules }),

  // Core parsing results
  verifiedDocResult: null,
  setVerifiedDocResult: (res) => set({ verifiedDocResult: res }),
  clearVerifiedDocResult: () => set({ verifiedDocResult: null }),

  gstParseResult: null,
  setGstParseResult: (res) => set({ gstParseResult: res }),
  clearGstParseResult: () => set({ gstParseResult: null }),

  udyamParseResult: null,
  setUdyamParseResult: (res) => set({ udyamParseResult: res }),
  clearUdyamParseResult: () => set({ udyamParseResult: null }),

  epfoParseResult: null,
  setEpfoParseResult: (res) => set({ epfoParseResult: res }),

  esicParseResult: null,
  setEsicParseResult: (res) => set({ esicParseResult: res }),

  startupParseResult: null,
  setStartupParseResult: (res) => set({ startupParseResult: res }),

  nsicParseResult: null,
  setNsicParseResult: (res) => set({ nsicParseResult: res }),

  technicalMatrixResult: null,
  setTechnicalMatrixResult: (res) => set({ technicalMatrixResult: res }),

  experienceResult: null,
  setExperienceResult: (res) => set({ experienceResult: res }),
  
  turnoverParseResult: null,
  setTurnoverParseResult: (res) => set({ turnoverParseResult: res }),
  clearTurnoverParseResult: () => set({ turnoverParseResult: null }),
  
  itrParseResult: null,
  setItrParseResult: (res) => set({ itrParseResult: res }),
  clearItrParseResult: () => set({ itrParseResult: null }),
  
  miiParseResult: null,
  setMiiParseResult: (res) => set({ miiParseResult: res }),
  clearMiiParseResult: () => set({ miiParseResult: null }),

  // NEW FOR GSTR3B & DEBARMENT
  gstr3bParseResult: null,
  setGstr3bParseResult: (res) => set({ gstr3bParseResult: res }),
  clearGstr3bParseResult: () => set({ gstr3bParseResult: null }),

  debarmentParseResult: null,
  setDebarmentParseResult: (res) => set({ debarmentParseResult: res }),
  clearDebarmentParseResult: () => set({ debarmentParseResult: null }),

  clearAllDocs: () => set({
    verifiedDocResult: null,
    gstParseResult: null,
    udyamParseResult: null,
    epfoParseResult: null,
    esicParseResult: null,
    startupParseResult: null,
    nsicParseResult: null,
    turnoverParseResult: null,
    itrParseResult: null,
    miiParseResult: null,
    gstr3bParseResult: null,
    debarmentParseResult: null,
    technicalMatrixResult: null,
    experienceResult: null,
    visualAuthResult: null,
  }),


  visualAuthResult: null,
  setVisualAuthResult: (res) => set({ visualAuthResult: res }),
  batchModeActive: false,
  setBatchModeActive: (active) => set({ batchModeActive: active }),

  // Compliance score block (e.g. wrong document uploaded for this bidder)
  complianceBlockedReason: null,
  setComplianceBlockedReason: (reason) => set({ complianceBlockedReason: reason }),
  clearComplianceBlock: () => set({ complianceBlockedReason: null }),
}));
