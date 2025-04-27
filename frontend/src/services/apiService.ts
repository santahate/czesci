import api from '../api/axios';
import { AxiosRequestConfig } from 'axios';

/**
 * Универсальный сервис для работы с API
 */
class ApiService {
  /**
   * GET запрос
   * @param url - эндпоинт API
   * @param config - дополнительные настройки запроса
   */
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await api.get<T>(url, config);
    return response.data;
  }

  /**
   * POST запрос
   * @param url - эндпоинт API
   * @param data - данные для отправки
   * @param config - дополнительные настройки запроса
   */
  async post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await api.post<T>(url, data, config);
    return response.data;
  }

  /**
   * PUT запрос
   * @param url - эндпоинт API
   * @param data - данные для отправки
   * @param config - дополнительные настройки запроса
   */
  async put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await api.put<T>(url, data, config);
    return response.data;
  }

  /**
   * DELETE запрос
   * @param url - эндпоинт API
   * @param config - дополнительные настройки запроса
   */
  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await api.delete<T>(url, config);
    return response.data;
  }

  /**
   * PATCH запрос
   * @param url - эндпоинт API
   * @param data - данные для отправки
   * @param config - дополнительные настройки запроса
   */
  async patch<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response = await api.patch<T>(url, data, config);
    return response.data;
  }
}

// Экспортируем экземпляр сервиса для использования в проекте
export default new ApiService();
