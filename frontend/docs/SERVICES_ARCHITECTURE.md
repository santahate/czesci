# Архитектура Сервисов

## Обзор

В проекте применяется сервис-ориентированная архитектура для работы с API. Вместо прямых вызовов axios в компонентах, мы используем сервисы как абстракцию для взаимодействия с бэкендом.

## Основные принципы

1. **Разделение ответственности** - компоненты отвечают за UI, сервисы - за взаимодействие с API
2. **Инкапсуляция** - детали работы с API скрыты внутри сервисов
3. **Типизация** - все запросы и ответы имеют четкие интерфейсы
4. **Повторное использование** - сервисы могут использоваться в разных компонентах
5. **Легкость тестирования** - можно создавать mock-сервисы для тестирования компонентов

## Структура сервисов

Все сервисы находятся в директории `src/services/`:

- `apiService.ts` - базовый сервис для работы с API (get, post, put, delete, patch)
- `authService.ts` - сервис для аутентификации и управления пользователем
- Другие сервисы по функциональным направлениям

## Базовый API-сервис

`apiService.ts` предоставляет универсальные методы для работы с API:

```typescript
// Примеры использования
import apiService from '../services/apiService';

// GET запрос с типизацией
const data = await apiService.get<UserData>('users/me');

// POST запрос с данными
const result = await apiService.post<CreateResponse>('items', { name: 'New Item' });
```

## Специализированные сервисы

Специализированные сервисы используют `apiService` и предоставляют методы для конкретных доменных областей:

```typescript
// Пример использования authService
import authService from '../services/authService';

// Вход пользователя
const user = await authService.login({ username, password });

// Проверка аутентификации
const isLoggedIn = await authService.isAuthenticated();

// Получение данных пользователя
const userData = await authService.getCurrentUser();
```

## Создание новых сервисов

При создании нового сервиса следуйте этим шагам:

1. Создайте файл в директории `src/services/` с именем `[название]Service.ts`
2. Определите интерфейсы для запросов и ответов
3. Создайте класс с методами для работы с API
4. Экспортируйте экземпляр класса

Пример структуры нового сервиса:

```typescript
import apiService from './apiService';

// Интерфейсы для типизации
interface ProductData {
  id: number;
  name: string;
  price: number;
}

// Класс сервиса
class ProductService {
  // Получение списка продуктов
  async getProducts(): Promise<ProductData[]> {
    return apiService.get<ProductData[]>('products/');
  }
  
  // Получение продукта по ID
  async getProduct(id: number): Promise<ProductData> {
    return apiService.get<ProductData>(`products/${id}/`);
  }
  
  // Создание продукта
  async createProduct(data: Omit<ProductData, 'id'>): Promise<ProductData> {
    return apiService.post<ProductData>('products/', data);
  }
}

// Экспорт экземпляра
export default new ProductService();
```

## Преимущества подхода

1. **Единая точка изменений** - при изменении API достаточно обновить только сервис
2. **Чистый код компонентов** - компоненты содержат только логику представления
3. **Типобезопасность** - все запросы и ответы имеют четкие типы
4. **Обработка ошибок** - можно реализовать специфичную обработку для каждого типа запроса
5. **Документация** - методы сервисов документируют доступные API-вызовы 