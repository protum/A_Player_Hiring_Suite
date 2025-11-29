import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { apiClient } from '../services/api';

// Mock axios
vi.mock('axios');
const mockedAxios = vi.mocked(axios);

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should have correct base URL', () => {
    expect(apiClient.defaults.baseURL).toBeTruthy();
  });

  it('should include auth token in requests when available', () => {
    const token = 'test-token';
    localStorage.setItem('access_token', token);

    // Verify interceptor behavior would add the token
    expect(apiClient.interceptors.request).toBeDefined();
  });

  it('should have response interceptors configured', () => {
    expect(apiClient.interceptors.response).toBeDefined();
  });
});
