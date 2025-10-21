# ISS Profile Mini App

Мини-приложение для Telegram бота, отображающее профиль пользователя ISS.

## 🚀 Развертывание

### На Render.com (рекомендуется)

1. **Создайте аккаунт** на [render.com](https://render.com)

2. **Загрузите файлы** на GitHub:
   - `app.py` (Flask сервер)
   - `index.html` (главная страница)
   - `points.html` (страница очков)
   - `settings.html` (страница настроек)
   - `styles.css`
   - `src/iss.svg` (логотип ISS)
   - `src/points.svg` (иконка очков)
   - `requirements.txt`
   - `runtime.txt`
   - `Procfile` (для production deployment)
   - `users_data.json` (данные пользователей)

3. **Создайте новый Web Service**:
   - Выберите репозиторий на GitHub
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (или оставьте пустым, если есть Procfile)

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

- ✅ Отображение имени и username из профиля ISS
- ✅ Центрированный логотип ISS
- ✅ Блок с очками (Points) - заглушка для будущих нововведений
- ✅ Блок с погодой из модуля Arc Weather
- ✅ Информация "Обо мне" (город, дата регистрации)
- ✅ Разделение данных из Telegram и ISS
- ✅ Кнопка "Поделиться профилем"
- ✅ **Нижнее меню навигации с переходами на отдельные страницы**
- ✅ **Отдельная страница Points (/points)**
- ✅ **Отдельная страница Настройки (/settings)**
- ✅ Чистый черный дизайн
- ✅ Адаптивный дизайн
- ✅ Поддержка темной темы Telegram

## 🎨 Дизайн

- Чистый черный фон без градиентов
- Центрированный SVG логотип ISS
- Большой тонкий шрифт для имени пользователя
- Организованная иерархия информации
- Полноширинная кнопка действия
- Мобильная адаптация
- Минималистичный интерфейс

## 🔧 Кастомизация

Mini App автоматически получает данные пользователя через Telegram Web App API и дополняет их через внутренний API бота.

### API Endpoints

- `GET /api/user-profile?user_id={telegram_user_id}` - получение данных профиля пользователя
- `GET /api/weather` - получение данных о погоде (использует модуль Arc Weather)
- `GET /api/user-settings?user_id={telegram_user_id}` - получение настроек пользователя
- `POST /api/user-settings` - обновление настроек пользователя
- `GET /api/debug` - отладочная информация (доступно только для разработки)

### Структура данных

**Профиль пользователя:**
```json
{
  "name": "Имя пользователя",
  "username": "username",
  "city": "Москва",
  "registration_date": "2024-01-15T10:30:00Z"
}
```

**Погода:**
```json
{
  "city": "Москва",
  "temperature": 12,
  "condition": "Переменная облачность",
  "feels_like": 10
}
```

**Настройки пользователя:**
```json
{
  "streaming_enabled": true,
  "updates_enabled": true,
  "changes_enabled": true,
  "promo_enabled": true
}
```

## 🐛 Troubleshooting

### Проблемы с данными профиля
Если Mini App показывает только имя и username:

1. **Проверьте отладку**: Откройте `https://your-app.onrender.com/api/debug` в браузере
2. **Проверьте логи**: В консоли Render.com посмотрите логи API запросов
3. **Проверьте user_id**: Убедитесь, что user_id из Telegram совпадает с ключами в `users_data.json`
4. **Проверьте файл**: Убедитесь, что `users_data.json` загружен на Render.com

### Проблемы с портами на Render.com
Если видите "No open ports detected":
- Убедитесь, что приложение слушает на `0.0.0.0`
- Используйте переменную окружения `PORT` для указания порта
- Используйте Gunicorn вместо Flask development сервера

### Development vs Production
- **Development**: `python app.py` (только для локального тестирования)
- **Production**: `gunicorn app:app` (рекомендуется для Render.com)

### CORS ошибки
Если Mini App не может получить данные:
- Проверьте, что `flask-cors` установлен
- Убедитесь, что API endpoint возвращает правильные CORS headers

## 📋 Требования

- HTTPS соединение (обязательно для Telegram Mini Apps)
- Современный браузер с поддержкой CSS Grid и Flexbox
- Telegram Web App API
