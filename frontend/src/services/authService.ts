import apiService from './apiService';
import { LoginRequest, LoginResponse, User } from '../types/auth';

/**
 * Сервис для работы с аутентификацией
 */
class AuthService {
  /**
   * Вход в систему
   * @param credentials - данные для входа
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    return apiService.post<LoginResponse>('auth/login/', credentials);
  }

  /**
   * Выход из системы
   */
  async logout(): Promise<void> {
    return apiService.post('auth/logout/');
  }
  
  /**
   * Получение данных текущего пользователя
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      return await apiService.get<User>('auth/user/');
    } catch (error) {
      // Если запрос завершился с ошибкой, пользователь не аутентифицирован
      return null;
    }
  }
  
  /**
   * Проверка, аутентифицирован ли пользователь
   */
  async isAuthenticated(): Promise<boolean> {
    try {
      const user = await this.getCurrentUser();
      return !!user;
    } catch {
      return false;
    }
  }
}

export default new AuthService(); 