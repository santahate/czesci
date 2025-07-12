# Settings Page Implementation Plan

**Created:** 2025-07-12

---

## Checklist

### 📁 Управление планом
- [x] Создать данный файл-план и разместить его в `.ai/tasks/` для трекинга выполнения

### 🌐 Общие
- [x] Создать основной шаблон `users/settings.html` (контейнер + таб-бар HTMX)
- [ ] Добавить базовые маршруты в `urls.py` (settings, buyer, seller, phone-endpoints)
- [ ] Создать директорию `.ai/tasks/` (если отсутствует) и сохранять обновления плана ⬅️ (создано)

### 🖥️ Backend – Django
1. **Views**
   - [ ] `settings_view` – wrapper-шаблон
   - [ ] `buyer_settings_partial` – HTMX-фрагмент с формой/CTA + телефоны
   - [ ] `seller_settings_partial` – HTMX-фрагмент с формой/CTA + телефоны
   - [ ] `add_phone_view` – POST, создаёт PhoneNumber, отправляет OTP
   - [ ] `verify_phone_view` – POST, проверка OTP, пометка `is_verified`
   - [ ] `deactivate_phone_view` – POST, `is_active=False`

2. **Forms**
   - [ ] Наследники `BuyerRegistrationForm` / `SellerRegistrationForm` без полей пароля
   - [ ] Валидатор номера (E.164)

3. **Services**
   - [ ] Создать `users/services/phone.py` – генерация OTP, отправка SMS
   - [ ] Перенести общие функции из `registration.py` и `sms.py`

4. **Models / Migrations**
   - [ ] Проверить модель `PhoneNumber`; при необходимости миграция
   - [ ] Связать номера с профилем (FK), фильтрация `is_active=True`

5. **Tests**
   - [ ] Юнит-тесты view-логики (GET/POST, статусы 200/204)
   - [ ] Тесты формы валидации и OTP-процесса

### 🎨 Frontend – HTMX, Tailwind, Alpine.js
6. **Templates**
   - [ ] `buyer_settings_partial.html` – форма/CTA, таблица номеров, кнопка "+ Add"
   - [ ] `seller_settings_partial.html` – аналогично buyer
   - [ ] Переиспользовать/копировать `verify_phone.html`, registration partials

7. **JS/UX**
   - [ ] HTMX вкладки (уже добавлены), Alpine.js состояния (спиннеры)

8. **Tailwind UI**
   - [ ] Добавить/обновить классы в `styles.css`, тест в брейкпоинтах

### ⚙️ DevOps / Config
- [ ] Обновить `settings/constants.py` (`MAX_SMS_ATTEMPTS` и др.)
- [ ] Добавить новые пути в i18n при необходимости

### 📚 Documentation
- [ ] Обновить README / docs об эндпоинтах и шаблонах 