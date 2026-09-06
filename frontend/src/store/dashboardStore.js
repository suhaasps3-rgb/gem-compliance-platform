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

  gstParseResult: null,
  setGstParseResult: (res) => set({ gstParseResult: res }),

  udyamParseResult: null,
  setUdyamParseResult: (res) => set({ udyamParseResult: res }),

  // NEW: Additional document parsers
  epfoParseResult: null,
  setEpfoParseResult: (res) => set({ epfoParseResult: res }),

  esicParseResult: null,
  setEsicParseResult: (res) => set({ esicParseResult: res }),

  startupParseResult: null,
  setStartupParseResult: (res) => set({ startupParseResult: res }),

  nsicParseResult: null,
  setNsicParseResult: (res) => set({ nsicParseResult: res }),

  // NEW: Technical matrix and experience
  technicalMatrixResult: null,
  setTechnicalMatrixResult: (res) => set({ technicalMatrixResult: res }),

  experienceResult: null,
  setExperienceResult: (res) => set({ experienceResult: res }),
  
  // NEW: Batch processor mode
  batchModeActive: false,
  setBatchModeActive: (active) => set({ batchModeActive: active })
}));
