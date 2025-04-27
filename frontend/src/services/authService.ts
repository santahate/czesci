import apiService from './apiService';
import { LoginRequest, LoginResponse, User } from '../types/auth';

// Ключ для хранения в localStorage
const AUTH_USER_KEY = 'czesci_auth_user';
const AUTH_STATE_KEY = 'czesci_auth_state';

/**
 * Сервис для работы с аутентификацией
 */
class AuthService {
  private userCache: User | null = null;
  private fetchingUser = false;
  private userFetchPromise: Promise<User | null> | null = null;

  constructor() {
    // Инициализируем кэш из localStorage
    try {
      const storedUser = localStorage.getItem(AUTH_USER_KEY);
      if (storedUser) {
        this.userCache = JSON.parse(storedUser);
      }
    } catch (e) {
      // Если возникла ошибка при чтении из localStorage, очищаем кэш
      localStorage.removeItem(AUTH_USER_KEY);
      localStorage.removeItem(AUTH_STATE_KEY);
    }
  }

  /**
   * Вход в систему
   * @param credentials - данные для входа
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    // Очищаем кэш при логине
    this.userCache = null;

    const userData = await apiService.post<LoginResponse>('auth/login/', credentials);

    // Сохраняем данные пользователя
    this.userCache = userData;
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(userData));
    localStorage.setItem(AUTH_STATE_KEY, 'authenticated');

    return userData;
  }

  /**
   * Выход из системы
   */
  async logout(): Promise<void> {
    // Очищаем кэш при логауте
    this.userCache = null;
    localStorage.removeItem(AUTH_USER_KEY);
    localStorage.setItem(AUTH_STATE_KEY, 'unauthenticated');

    return apiService.post('auth/logout/');
  }

  /**
   * Получение данных текущего пользователя
   */
  async getCurrentUser(): Promise<User | null> {
    // Проверяем, известно ли нам, что пользователь не аутентифицирован
    if (localStorage.getItem(AUTH_STATE_KEY) === 'unauthenticated') {
      return null;
    }

    // Если запрос к API уже выполняется, возвращаем тот же промис
    if (this.fetchingUser && this.userFetchPromise) {
      return this.userFetchPromise;
    }

    // Если данные уже есть в кэше, возвращаем их
    if (this.userCache !== null) {
      return this.userCache;
    }

    // Отмечаем, что начали запрос
    this.fetchingUser = true;

    // Создаем промис запроса, чтобы повторные вызовы могли его переиспользовать
    this.userFetchPromise = new Promise<User | null>(resolve => {
      apiService
        .get<User>('auth/user/')
        .then(user => {
          this.userCache = user;
          localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));
          localStorage.setItem(AUTH_STATE_KEY, 'authenticated');
          resolve(user);
        })
        .catch(_error => {
          this.userCache = null;
          localStorage.removeItem(AUTH_USER_KEY);
          localStorage.setItem(AUTH_STATE_KEY, 'unauthenticated');
          resolve(null);
        })
        .finally(() => {
          this.fetchingUser = false;
          this.userFetchPromise = null;
        });
    });

    return this.userFetchPromise;
  }

  /**
   * Проверка, аутентифицирован ли пользователь
   */
  isAuthenticated(): boolean {
    return this.userCache !== null || localStorage.getItem(AUTH_STATE_KEY) === 'authenticated';
  }

  /**
   * Очистка кэша пользователя
   */
  clearUserCache() {
    this.userCache = null;
    localStorage.removeItem(AUTH_USER_KEY);
  }
}

export default new AuthService();
