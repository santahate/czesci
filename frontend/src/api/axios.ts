import axios, { AxiosError, AxiosResponse } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/';

interface CsrfResponse {
  csrf_token: string;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Add a request interceptor
api.interceptors.request.use(async config => {
  // Only add CSRF token for non-safe methods
  if (config.method !== 'get' && config.method !== 'head' && config.method !== 'options') {
    try {
      // Get CSRF token
      const csrfUrl = `${API_BASE_URL}auth/csrf/`;
      const response = await axios.get<CsrfResponse>(csrfUrl, {
        withCredentials: true,
      });
      // Add token to headers
      config.headers['X-CSRFToken'] = response.data.csrf_token;
    } catch (error) {
      console.error('Failed to fetch CSRF token:', error);
    }
  }
  return config;
});

// Add a response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Обработка общих ошибок
    if (error.response) {
      const status = error.response.status;

      // Обработка ошибок аутентификации
      if (status === 401) {
        console.error('Authentication error: Not authenticated');
        // Можно перенаправить на страницу логина
        // window.location.href = '/login';
      }

      // Обработка ошибок доступа
      else if (status === 403) {
        console.error('Authorization error: Access forbidden');
      }

      // Обработка серверных ошибок
      else if (status >= 500) {
        console.error('Server error:', error.response.data);
      }

      // Логирование всех ошибок
      console.error(`API Error ${status}:`, error.response.data);
    } else if (error.request) {
      // Ошибка, когда запрос был сделан, но ответ не получен
      console.error('Network error: No response received', error.request);
    } else {
      // Что-то случилось при настройке запроса
      console.error('Request error:', error.message);
    }

    return Promise.reject(error);
  }
);

export default api;
