import apiService from './apiService';

interface LoginRequest {
  username: string;
  password: string;
}

interface LoginResponse {
  username: string;
  email?: string;
  is_staff?: boolean;
}

interface UserData {
  username: string;
  email?: string;
  is_staff?: boolean;
}

interface CsrfResponse {
  csrf_token: string;
}

/**
 * Сервис для работы с аутентификацией
 */
class AuthService {
  /**
   * Получение CSRF токена
   */
  async getCsrfToken(): Promise<string> {
    const response = await apiService.get<CsrfResponse>('auth/csrf/');
    return response.csrf_token;
  }

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
  async getCurrentUser(): Promise<UserData | null> {
    try {
      return await apiService.get<UserData>('auth/user/');
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