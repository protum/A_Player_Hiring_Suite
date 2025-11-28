import axios from 'axios';
import type {
  Candidate,
  Scorecard,
  Interview,
  CEOAssessment,
  PowerScoreAssessment,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Candidates
export const candidatesApi = {
  list: () => api.get<Candidate[]>('/candidates'),
  create: (data: Partial<Candidate>) => api.post<Candidate>('/candidates', data),
  get: (id: string) => api.get<Candidate>(`/candidates/${id}`),
  update: (id: string, data: Partial<Candidate>) => api.put<Candidate>(`/candidates/${id}`, data),
  delete: (id: string) => api.delete(`/candidates/${id}`),
};

// Scorecards
export const scorecardsApi = {
  list: () => api.get<Scorecard[]>('/scorecards'),
  create: (data: Partial<Scorecard>) => api.post<Scorecard>('/scorecards', data),
  get: (id: string) => api.get<Scorecard>(`/scorecards/${id}`),
  update: (id: string, data: Partial<Scorecard>) => api.put<Scorecard>(`/scorecards/${id}`, data),
  delete: (id: string) => api.delete(`/scorecards/${id}`),
  exportPdf: (id: string) => api.get(`/scorecards/${id}/export/pdf`, { responseType: 'blob' }),
};

// Interviews
export const interviewsApi = {
  list: (candidateId?: string) => api.get<Interview[]>('/interviews', { params: { candidate_id: candidateId } }),
  create: (data: Partial<Interview>) => api.post<Interview>('/interviews', data),
  get: (id: string) => api.get<Interview>(`/interviews/${id}`),
  update: (id: string, data: Partial<Interview>) => api.put<Interview>(`/interviews/${id}`, data),
  delete: (id: string) => api.delete(`/interviews/${id}`),
  generateScript: (id: string) => api.post(`/interviews/${id}/generate-script`),
  addRedFlag: (id: string, data: any) => api.post(`/interviews/${id}/red-flags`, data),
  exportPdf: (id: string) => api.get(`/interviews/${id}/export/pdf`, { responseType: 'blob' }),
};

// CEO Assessments
export const ceoAssessmentsApi = {
  list: (subjectId?: string) => api.get<CEOAssessment[]>('/assessments/ceo', { params: { subject_id: subjectId } }),
  create: (data: Partial<CEOAssessment>) => api.post<CEOAssessment>('/assessments/ceo', data),
  get: (id: string) => api.get<CEOAssessment>(`/assessments/ceo/${id}`),
  delete: (id: string) => api.delete(`/assessments/ceo/${id}`),
  exportPdf: (id: string) => api.get(`/assessments/ceo/${id}/export/pdf`, { responseType: 'blob' }),
};

// Power Score Assessments
export const powerScoreApi = {
  list: (subjectId?: string) => api.get<PowerScoreAssessment[]>('/assessments/power-score', { params: { subject_id: subjectId } }),
  create: (data: Partial<PowerScoreAssessment>) => api.post<PowerScoreAssessment>('/assessments/power-score', data),
  get: (id: string) => api.get<PowerScoreAssessment>(`/assessments/power-score/${id}`),
  getTrends: (id: string) => api.get(`/assessments/power-score/${id}/trends`),
  delete: (id: string) => api.delete(`/assessments/power-score/${id}`),
  exportPdf: (id: string) => api.get(`/assessments/power-score/${id}/export/pdf`, { responseType: 'blob' }),
};

// System
export const systemApi = {
  health: () => api.get('/system/health'),
  exportBackup: (format: string) => api.post('/system/backup/export', null, { params: { format }, responseType: 'blob' }),
  importBackup: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/system/backup/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getStats: () => api.get('/system/stats'),
};

export default api;

// Ideal Team Player Assessments
export const idealTeamPlayerApi = {
  getQuestions: () => api.get('/assessments/ideal-team-player/questions'),
  list: (subjectId?: string) => api.get('/assessments/ideal-team-player', { params: { subject_id: subjectId } }),
  create: (data: any) => api.post('/assessments/ideal-team-player', data),
  get: (id: string) => api.get(`/assessments/ideal-team-player/${id}`),
  getInsights: (id: string) => api.get(`/assessments/ideal-team-player/${id}/insights`),
  delete: (id: string) => api.delete(`/assessments/ideal-team-player/${id}`),
  exportPdf: (id: string) => api.get(`/assessments/ideal-team-player/${id}/export/pdf`, { responseType: 'blob' }),
};

// Core Values Assessments
export const coreValuesApi = {
  getQuestions: () => api.get('/assessments/core-values/questions'),
  list: (subjectId?: string) => api.get('/assessments/core-values', { params: { subject_id: subjectId } }),
  create: (data: any) => api.post('/assessments/core-values', data),
  get: (id: string) => api.get(`/assessments/core-values/${id}`),
  getInsights: (id: string) => api.get(`/assessments/core-values/${id}/insights`),
  delete: (id: string) => api.delete(`/assessments/core-values/${id}`),
  exportPdf: (id: string) => api.get(`/assessments/core-values/${id}/export/pdf`, { responseType: 'blob' }),
};
