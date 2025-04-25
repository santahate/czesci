import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true
});

// Add a request interceptor
api.interceptors.request.use(async (config) => {
  // Only add CSRF token for non-safe methods
  if (config.method !== 'get' && config.method !== 'head' && config.method !== 'options') {
    try {
      // Get CSRF token
      const response = await axios.get('http://localhost:8000/api/auth/csrf/', {
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