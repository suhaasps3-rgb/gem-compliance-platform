// src/store/dashboardStore.js
import { create } from 'zustand';

// Zustand store for global dashboard state
export const useDashboardStore = create((set, get) => ({
  // Currently selected document tab: 'tender' | 'gst' | 'udyam'
  selectedDocument: 'tender',
  setSelectedDocument: (doc) => set({ selectedDocument: doc }),

  // Reference to the PDF viewer (exposes goToPage)
  viewerRef: null,
  setViewerRef: (ref) => set({ viewerRef: ref }),

  // Client-only audit log (SHA-256 entries)
  auditLog: [],
  addAuditEntry: (entry) => set({ auditLog: [...get().auditLog, entry] }),

  // Dynamic tender rules compiled from officer uploads
  tenderRules: [],
  setTenderRules: (rules) => set({ tenderRules: rules }),

  // Result from verifying an uploaded bidder document (bypasses dropdown)
  verifiedDocResult: null,
  setVerifiedDocResult: (result) => set({ verifiedDocResult: result }),
  clearVerifiedDocResult: () => set({ verifiedDocResult: null }),

  // Results from parsing GST / Udyam certificates
  gstParseResult: null,
  setGstParseResult: (result) => set({ gstParseResult: result }),
  clearGstParseResult: () => set({ gstParseResult: null }),

  udyamParseResult: null,
  setUdyamParseResult: (result) => set({ udyamParseResult: result }),
  clearUdyamParseResult: () => set({ udyamParseResult: null }),
}));
