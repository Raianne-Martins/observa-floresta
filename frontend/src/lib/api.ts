/**
 * Cliente HTTP para comunicação com o backend
 */
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para logging (desenvolvimento)
if (process.env.NEXT_PUBLIC_ENVIRONMENT === 'development') {
  api.interceptors.request.use(
    (config) => {
      console.log('🔵 API Request:', config.method?.toUpperCase(), config.url);
      return config;
    },
    (error) => {
      console.error('🔴 API Request Error:', error);
      return Promise.reject(error);
    }
  );

  api.interceptors.response.use(
    (response) => {
      console.log('🟢 API Response:', response.status, response.config.url);
      return response;
    },
    (error) => {
      console.error('🔴 API Response Error:', error.response?.status, error.config?.url);
      return Promise.reject(error);
    }
  );
}

export default api;
