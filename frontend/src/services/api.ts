import axios from 'axios';

const API_BASE = '/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('claimsight_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle 401s
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if invalid
      if (window.location.pathname !== '/login') {
        localStorage.removeItem('claimsight_token');
        localStorage.removeItem('claimsight_user');
      }
    }
    return Promise.reject(error);
  }
);

export const api = {
  // Auth
  login: (credentials: { email: string; password: string }) =>
    apiClient.post('/auth/login', credentials),
  register: (userData: any) => apiClient.post('/auth/register', userData),
  getMe: () => apiClient.get('/auth/me'),

  // Claims
  getClaims: (params?: any) => apiClient.get('/claims', { params }),
  getClaim: (claimId: string) => apiClient.get(`/claims/${claimId}`),
  createClaim: (claimData: any) => apiClient.post('/claims', claimData),
  updateClaim: (claimId: string, data: any) => apiClient.patch(`/claims/${claimId}`, data),
  deleteClaim: (claimId: string) => apiClient.delete(`/claims/${claimId}`),

  // Evidence
  getEvidence: (claimId: string) => apiClient.get(`/claims/${claimId}/evidence`),
  getEvidenceDetail: (evidenceId: string) => apiClient.get(`/evidence/${evidenceId}`),
  uploadEvidence: (claimId: string, formData: FormData) =>
    apiClient.post(`/claims/${claimId}/evidence`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  deleteEvidence: (evidenceId: string) => apiClient.delete(`/evidence/${evidenceId}`),

  // Investigation & React Flow Graph
  runInvestigation: (claimId: string) => apiClient.post(`/claims/${claimId}/investigate`),
  getInvestigationSummary: (claimId: string) => apiClient.get(`/claims/${claimId}/investigation`),
  getYoloDetection: (claimId: string) => apiClient.get(`/claims/${claimId}/yolo-detection`),
  getTimeline: (claimId: string) => apiClient.get(`/claims/${claimId}/timeline`),
  getHypotheses: (claimId: string) => apiClient.get(`/claims/${claimId}/hypotheses`),
  getWitnesses: (claimId: string) => apiClient.get(`/claims/${claimId}/witnesses`),
  getRelationshipGraph: (claimId: string) => apiClient.get(`/claims/${claimId}/relationships`),

  // Evaluation & Counterfactual Sandbox
  getEvaluation: (claimId: string) => apiClient.get(`/claims/${claimId}/evaluation`),
  recomputeEvaluation: (claimId: string) => apiClient.post(`/claims/${claimId}/evaluate`),
  runCounterfactual: (claimId: string, assumption: string) =>
    apiClient.post(`/claims/${claimId}/counterfactual`, { assumption }),
  getBenchmarks: (claimId: string) => apiClient.get(`/claims/${claimId}/benchmarks`),

  // Next-Best-Evidence
  getRecommendations: (claimId: string) => apiClient.get(`/claims/${claimId}/evidence-recommendations`),
  createEvidenceRequest: (claimId: string, data: any) =>
    apiClient.post(`/claims/${claimId}/evidence-requests`, data),
  updateEvidenceRequest: (requestId: string, data: any) =>
    apiClient.patch(`/evidence-requests/${requestId}`, data),

  // Policy & Settlement
  getCoverage: (claimId: string) => apiClient.get(`/claims/${claimId}/coverage`),
  getSettlementRecommendation: (claimId: string) =>
    apiClient.get(`/claims/${claimId}/settlement-recommendation`),

  // Decisions & Audits
  recordDecision: (claimId: string, data: any) => apiClient.post(`/claims/${claimId}/decisions`, data),
  addNote: (claimId: string, note: string) => apiClient.post(`/claims/${claimId}/notes`, { note }),
  getAuditTrail: (claimId: string) => apiClient.get(`/claims/${claimId}/audit`),

  // Analytics
  getDashboardAnalytics: () => apiClient.get('/analytics/dashboard'),

  // Reports
  getAllReports: () => apiClient.get('/reports'),
  generateReport: (claimId: string) => apiClient.post(`/claims/${claimId}/reports`),
  downloadReportUrl: (claimId: string) => `/api/reports/${claimId}/download`,
  downloadFirReportUrl: (claimId: string) => `/api/reports/${claimId}/fir-download`,
  downloadSiuPdf: async (claimId: string) => {
    const response = await apiClient.get(`/reports/${claimId}/download`, {
      responseType: 'blob',
    });
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', `CLAIMSIGHT_Investigation_Report_${claimId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => window.URL.revokeObjectURL(downloadUrl), 2000);
  },
  downloadFirPdf: async (claimId: string) => {
    const response = await apiClient.get(`/reports/${claimId}/fir-download`, {
      responseType: 'blob',
    });
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', `Official_Police_FIR_GD_${claimId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => window.URL.revokeObjectURL(downloadUrl), 2000);
  },
};

