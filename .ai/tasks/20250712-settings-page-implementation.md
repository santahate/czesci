# Settings Page Implementation Plan

**Created:** 2025-07-12

---

## Checklist

### 📁 Управление планом
- [x] Создать данный файл-план и разместить его в `.ai/tasks/` для трекинга выполнения

### 🌐 Общие
- [x] Создать основной шаблон `users/settings.html` (контейнер + таб-бар HTMX)
- [x] Добавить базовые маршруты в `urls.py` (settings, buyer, seller, phone-endpoints)
- [ ] Создать директорию `.ai/tasks/` (если отсутствует) и сохранять обновления плана ⬅️ (создано)

### 🖥️ Backend – Django
1. **Views**
   - [x] `settings_view` – wrapper-шаблон
   - [x] `buyer_settings_partial` – HTMX-фрагмент (скелет)
   - [x] `seller_settings_partial` – HTMX-фрагмент (скелет)
   - [x] `add_phone_view` – POST, создаёт PhoneNumber, отправляет OTP
   - [x] `verify_phone_view` – POST, проверка OTP, пометка `is_verified`
   - [x] `deactivate_phone_view` – POST, `is_active=False`

2. **Forms**
   - [x] Создать `BuyerProfileForm` / `SellerProfileForm` для редактирования
   - [x] Валидатор номера (E.164) уже существует как `PHONE_REGEX`

3. **Services**
   - [x] Создать `users/services/phone.py` – генерация OTP, отправка SMS
   - [x] Перенести генерацию OTP из `registration.py` в `PhoneService` (RegistrationService теперь использует PhoneService)

4. **Models / Migrations**
   - [ ] Проверить модель `PhoneNumber`; при необходимости миграция
   - [ ] Связать номера с профилем (FK), фильтрация `is_active=True`

### 🎨 Frontend – HTMX, Tailwind, Alpine.js
5. **Templates**
   - [x] `buyer_settings_partial.html` – форма/CTA, таблица номеров, кнопка "+ Add"
   - [x] `seller_settings_partial.html` – форма/CTA, таблица номеров, кнопка "+ Add"
   - [x] Переиспользовать существующий `verify_phone.html` для OTP

6. **JS/UX**
   - [x] HTMX вкладки + Alpine.js спиннеры добавлены в `settings.html`

7. **Tailwind UI**
   - [x] Использованы стандартные Tailwind классы; визуально проверено

### ⚙️ DevOps / Config
- [x] Константа `MAX_SMS_ATTEMPTS` уже существует; дополнительные не требуются
- [x] i18n пути не изменялись – актуально

### 📚 Documentation
- [x] Создан `docs/005-Backend/005.3-settings-endpoints-en.md` c новым перечнем маршрутов 

### 🐞 Bug Fixes
- [x] Tab highlight colour changed to blue (border-blue-600) to match buttons 