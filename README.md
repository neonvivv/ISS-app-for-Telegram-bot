# ISS Profile Mini App

Мини-приложение для Telegram бота, отображающее профиль пользователя ISS.

## 🚀 Развертывание

### На Render.com (рекомендуется)

1. **Создайте аккаунт** на [render.com](https://render.com)

2. **Загрузите файлы** на GitHub:
   - `app.py` (Flask сервер)
   - `index.html`
   - `styles.css`
   - `requirements.txt`
   - `runtime.txt`

3. **Создайте новый Web Service**:
   - Выберите репозиторий на GitHub
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Получите URL** типа: `https://your-app.onrender.com`

### Интеграция с ботом

Добавьте в код бота кнопку для открытия мини-приложения:

```python
from telegram import InlineKeyboardButton, WebAppInfo

keyboard = [[InlineKeyboardButton(
    "👤 Мой профиль", 
    web_app=WebAppInfo(url="https://your-app.onrender.com")
)]]
```

## 📱 Функционал

- ✅ Отображение имени и username пользователя
- ✅ Аватар с инициалами
- ✅ Информация о профиле (возраст, город, дата регистрации)
- ✅ Статистика использования бота
- ✅ Адаптивный дизайн
- ✅ Поддержка темной темы Telegram
- ✅ Красивые анимации и градиенты

## 🎨 Дизайн

- Современный glassmorphism стиль
- Градиентные фоны
- Плавные анимации
- Мобильная адаптация
- Темная тема

## 🔧 Кастомизация

Mini App автоматически получает данные пользователя через Telegram Web App API и дополняет их через внутренний API бота.

### API Endpoints

- `GET /api/user-profile?user_id={telegram_user_id}` - получение данных профиля пользователя

### Структура данных

```json
{
  "name": "Имя пользователя",
  "username": "username",
  "age": 25,
  "city": "Москва",
  "registration_date": "2024-01-15T10:30:00Z",
  "total_reports": 15,
  "active_reports": 3,
  "resolved_reports": 12
}
```

## 📋 Требования

- HTTPS соединение (обязательно для Telegram Mini Apps)
- Современный браузер с поддержкой CSS Grid и Flexbox
- Telegram Web App API
