/**
 * API service for making HTTP requests to the backend
 */
import axios from 'axios';
import type { AuthTokens, User, Scorecard, CEOScorecard, Interview, LeadershipAssessment, PowerScore } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email: string, password: string): Promise<AuthTokens> => {
    const response = await api.post('/api/v1/auth/login', { email, password });
    return response.data;
  },

  register: async (userData: { email: string; password: string; full_name: string }): Promise<User> => {
    const response = await api.post('/api/v1/auth/register', userData);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/v1/auth/me');
    return response.data;
  },
};

// Scorecards API
export const scorecardsAPI = {
  list: async (): Promise<Scorecard[]> => {
    const response = await api.get('/api/v1/scorecards');
    return response.data;
  },

  get: async (id: string): Promise<Scorecard> => {
    const response = await api.get(`/api/v1/scorecards/${id}`);
    return response.data;
  },

  create: async (data: Partial<Scorecard>): Promise<Scorecard> => {
    const response = await api.post('/api/v1/scorecards', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Scorecard>): Promise<Scorecard> => {
    const response = await api.put(`/api/v1/scorecards/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/v1/scorecards/${id}`);
  },
};

// CEO Scorecards API
export const ceoScorecardsAPI = {
  list: async (): Promise<CEOScorecard[]> => {
    const response = await api.get('/api/v1/ceo-scorecards');
    return response.data;
  },

  get: async (id: string): Promise<CEOScorecard> => {
    const response = await api.get(`/api/v1/ceo-scorecards/${id}`);
    return response.data;
  },

  create: async (data: Partial<CEOScorecard>): Promise<CEOScorecard> => {
    const response = await api.post('/api/v1/ceo-scorecards', data);
    return response.data;
  },

  update: async (id: string, data: Partial<CEOScorecard>): Promise<CEOScorecard> => {
    const response = await api.put(`/api/v1/ceo-scorecards/${id}`, data);
    return response.data;
  },

  finalize: async (id: string): Promise<CEOScorecard> => {
    const response = await api.post(`/api/v1/ceo-scorecards/${id}/finalize`);
    return response.data;
  },

  getExcellenceIndex: async (id: string) => {
    const response = await api.get(`/api/v1/ceo-scorecards/${id}/excellence-index`);
    return response.data;
  },

  getRecommendations: async (id: string) => {
    const response = await api.get(`/api/v1/ceo-scorecards/${id}/recommendations`);
    return response.data;
  },
};

// Interviews API
export const interviewsAPI = {
  list: async (): Promise<Interview[]> => {
    const response = await api.get('/api/v1/interviews');
    return response.data;
  },

  get: async (id: string): Promise<Interview> => {
    const response = await api.get(`/api/v1/interviews/${id}`);
    return response.data;
  },

  create: async (data: Partial<Interview>): Promise<Interview> => {
    const response = await api.post('/api/v1/interviews', data);
    return response.data;
  },

  getRedFlags: async (id: string) => {
    const response = await api.get(`/api/v1/interviews/${id}/red-flags`);
    return response.data;
  },
};

// Leadership Assessments API
export const leadershipAPI = {
  list: async (): Promise<LeadershipAssessment[]> => {
    const response = await api.get('/api/v1/leadership/assessments');
    return response.data;
  },

  get: async (id: string): Promise<LeadershipAssessment> => {
    const response = await api.get(`/api/v1/leadership/assessments/${id}`);
    return response.data;
  },

  create: async (data: Partial<LeadershipAssessment>): Promise<LeadershipAssessment> => {
    const response = await api.post('/api/v1/leadership/assessments', data);
    return response.data;
  },
};

// Power Scores API
export const powerScoresAPI = {
  list: async (): Promise<PowerScore[]> => {
    const response = await api.get('/api/v1/power-scores');
    return response.data;
  },

  get: async (id: string): Promise<PowerScore> => {
    const response = await api.get(`/api/v1/power-scores/${id}`);
    return response.data;
  },

  create: async (data: Partial<PowerScore>): Promise<PowerScore> => {
    const response = await api.post('/api/v1/power-scores', data);
    return response.data;
  },

  getWeakestLink: async (id: string) => {
    const response = await api.get(`/api/v1/power-scores/${id}/weakest-link`);
    return response.data;
  },
};

export default api;
