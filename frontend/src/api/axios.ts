import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true
});

// Add a request interceptor
api.interceptors.request.use(async (config) => {
  // Only add CSRF token for non-safe methods
  if (config.method !== 'get' && config.method !== 'head' && config.method !== 'options') {
    try {
      // Get CSRF token
      const csrfUrl = `${API_BASE_URL}auth/csrf/`;
      const response = await axios.get(csrfUrl, {
        withCredentials: true
      });
      const csrfToken = response.data.csrf_token;
      
      // Add token to headers
      config.headers['X-CSRFToken'] = csrfToken;
    } catch (error) {
      console.error('Failed to fetch CSRF token:', error);
    }
  }
  return config;
});

export default api; 