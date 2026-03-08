# 📖 D3M VPN MiniApp - Документация

## 📑 Содержание

1. [Введение](#введение)
2. [Архитектура](#архитектура)
3. [Быстрый старт](#быстрый-старт)
4. [Настройка окружения](#настройка-окружения)
5. [Запуск проекта](#запуск-проекта)
6. [Интеграция с Telegram](#интеграция-s-telegram)
7. [Интеграция с RemnaWave](#интеграция-s-remnawave)
8. [API Документация](#api-документация)
9. [Структура проекта](#структура-проекта)
10. [Разработка](#разработка)
11. [Деплой](#деплой)
12. [Troubleshooting](#troubleshooting)

---

## Введение

**D3M VPN MiniApp** — это Telegram MiniApp для управления VPN-подписками на основе бота RemnaShop.

### Возможности

- ✅ Аутентификация через Telegram
- ✅ Просмотр и управление подпиской
- ✅ Управление устройствами
- ✅ Выбор и покупка тарифов
- ✅ Активация промокодов
- ✅ Реферальная программа
- ✅ Статистика использования трафика
- ✅ Интеграция с RemnaWave API
- ✅ Полная синхронизация с базой данных

### Технологии

**Backend:**
- FastAPI (Python 3.12)
- SQLAlchemy (Async)
- PostgreSQL
- Redis
- JWT Authentication

**Frontend:**
- React 18
- TypeScript
- Bootstrap 5
- Zustand (state management)
- React Router
- Axios

**DevOps:**
- Docker & Docker Compose
- Nginx (reverse proxy)

---

## Архитектура

```
┌─────────────────┐
│  Telegram Web   │
│   (MiniApp)     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│     Nginx       │
│  (Reverse Proxy)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│Frontend │ │ Backend  │
│ (React) │ │ (FastAPI)│
└─────────┘ └────┬─────┘
                 │
           ┌─────┴──────┐
           │            │
           ▼            ▼
      ┌────────┐   ┌────────┐
      │Postgres│   │ Redis  │
      │   DB   │   │ Cache  │
      └────┬───┘   └────────┘
           │
           ▼
      ┌──────────┐
      │RemnaWave │
      │   API    │
      └──────────┘
```

---

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/d3m-vpn-miniapp.git
cd d3m-vpn-miniapp
```

### 2. Настройка окружения

```bash
# Копируем файл с примером переменных окружения
cp .env.example .env

# Открываем и редактиируем .env
nano .env
```

### 3. Запуск через Docker Compose

```bash
# Запуск всех сервисов
docker compose up -d

# Проверка статуса
docker compose ps

# Просмотр логов
docker compose logs -f
```

### 4. Проверка работы

- **Frontend:** http://localhost
- **Backend API:** http://localhost/api/v1
- **API Docs:** http://localhost/docs
- **Health Check:** http://localhost/health

---

## Настройка окружения

### Переменные окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
# Application
APP_DOMAIN=vpn.yourdomain.com      # Домен вашего приложения
APP_HOST=0.0.0.0
APP_PORT=80

# Bot (получите у @BotFather)
BOT_TOKEN=123456:ABC-DEF1234...    # Токен бота
BOT_SECRET_TOKEN=your-secret-token # Секрет для вебхуков
BOT_SUPPORT_USERNAME=support       # Username поддержки

# RemnaWave API
REMNAWAVE_HOST=api.remnawave.com   # Хост RemnaWave
REMNAWAVE_PORT=443
REMNAWAVE_TOKEN=your-token         # Токен RemnaWave
REMNAWAVE_WEBHOOK_SECRET=secret    # Секрет вебхуков

# Database
DATABASE_NAME=d3mvpn
DATABASE_USER=d3mvpn
DATABASE_PASSWORD=secure-password  # Надёжный пароль

# Redis
REDIS_PASSWORD=secure-redis-pass   # Надёжный пароль

# JWT
JWT_SECRET_KEY=your-jwt-secret     # Секрет для JWT
```

### Генерация секретных ключей

```bash
# Генерация SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Генерация пароля
openssl rand -base64 32
```

---

## Запуск проекта

### Команды управления

Используйте скрипт `Makefile.sh`:

```bash
# Запуск
./Makefile.sh start

# Остановка
./Makefile.sh stop

# Перезапуск
./Makefile.sh restart

# Просмотр логов
./Makefile.sh logs backend
./Makefile.sh logs frontend

# Пересборка
./Makefile.sh rebuild

# Очистка (удаление volumes)
./Makefile.sh clean

# Режим разработки
./Makefile.sh dev
```

### Ручные команды Docker

```bash
# Запуск
docker compose up -d

# Остановка
docker compose down

# Пересборка
docker compose build --no-cache
docker compose up -d

# Логи
docker compose logs -f backend
docker compose logs -f frontend

# Очистка
docker compose down -v
```

---

## Интеграция с Telegram

### 1. Создание бота

1. Откройте @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Сохраните полученный токен

### 2. Настройка MiniApp

1. В @BotFather отправьте `/mybots`
2. Выберите вашего бота
3. Перейдите в `Bot Settings` → `Menu Button`
4. Выберите `Configure Menu Button`
5. Отправьте URL вашего MiniApp: `https://your-domain.com`
6. Укажите название кнопки

### 3. Получение данных пользователя

MiniApp автоматически получает данные из `window.Telegram.WebApp.initDataUnsafe`:

```typescript
const tg = window.Telegram.WebApp;
const user = tg.initDataUnsafe.user;
const startParam = tg.initDataUnsafe.start_param; // Реферальный параметр
```

### 4. Аутентификация

Frontend отправляет `initData` на backend для верификации:

```typescript
// Отправка данных для аутентификации
const response = await apiClient.post('/auth/init', initData);
const { access_token } = response.data;
```

---

## Интеграция с RemnaWave

### Настройка подключения

1. Получите токен RemnaWave API из панели управления
2. Настройте переменные окружения:

```env
REMNAWAVE_HOST=api.remnawave.com
REMNAWAVE_PORT=443
REMNAWAVE_TOKEN=your-api-token
REMNAWAVE_WEBHOOK_SECRET=your-webhook-secret
```

### Синхронизация данных

Backend автоматически синхронизирует данные с RemnaWave:

- Пользователи
- Подписки
- Устройства
- Тарифные планы
- Использование трафика

---

## API Документация

### Базовый URL

```
https://your-domain.com/api/v1
```

### Аутентификация

Все запросы (кроме `/auth/init`) требуют заголовок:

```
Authorization: Bearer <access_token>
X-Telegram-ID: <telegram_user_id>
```

### Endpoints

#### Authentication

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/auth/init` | Инициализация сессии |
| GET | `/auth/me` | Текущий пользователь |
| POST | `/auth/logout` | Выход |

#### Users

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/users/me` | Профиль пользователя |
| PUT | `/users/me` | Обновление профиля |
| GET | `/users/me/referrals` | Статистика рефералов |

#### Subscriptions

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/subscriptions` | Все подписки |
| GET | `/subscriptions/active` | Активная подписка |
| GET | `/subscriptions/{id}` | Подписка по ID |
| POST | `/subscriptions/{id}/renew` | Продление |
| GET | `/subscriptions/{id}/traffic` | Использование трафика |

#### Devices

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/devices` | Список устройств |
| POST | `/devices` | Добавить устройство |
| DELETE | `/devices/{id}` | Удалить устройство |
| POST | `/devices/reset` | Сброс устройств |

#### Plans

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/plans` | Список тарифов |
| GET | `/plans/{id}` | Тариф по ID |

### Примеры запросов

#### Получение активной подписки

```bash
curl -X GET "https://your-domain.com/api/v1/subscriptions/active" \
  -H "Authorization: Bearer <token>" \
  -H "X-Telegram-ID: 123456789"
```

#### Добавление устройства

```bash
curl -X POST "https://your-domain.com/api/v1/devices" \
  -H "Authorization: Bearer <token>" \
  -H "X-Telegram-ID: 123456789" \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone"}'
```

---

## Структура проекта

```
d3m-vpn-miniapp/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── user.py
│   │   │   │   │   ├── subscription.py
│   │   │   │   │   ├── device.py
│   │   │   │   │   └── plan.py
│   │   │   │   └── router.py
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── exceptions.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── init.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── subscription.py
│   │   │   ├── transaction.py
│   │   │   ├── plan.py
│   │   │   └── device.py
│   │   ├── schemas/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── user.py
│   │   │   ├── subscription.py
│   │   │   ├── device.py
│   │   │   ├── plan.py
│   │   │   └── remnawave.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── subscription/
│   │   │   ├── device/
│   │   │   ├── plan/
│   │   │   └── payment/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── types/
│   │   └── utils/
│   ├── Dockerfile
│   └── package.json
├── nginx/
│   ├── nginx.conf
│   └── ssl/
├── docker-compose.yml
├── .env.example
└── Makefile.sh
```

---

## Разработка

### Режим разработки

```bash
# Запуск в режиме разработки
./Makefile.sh dev

# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Backend разработка

```bash
cd backend

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend разработка

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск сервера разработки
npm run dev
```

---

## Деплой

### Требования

- Ubuntu 20.04+ / Debian 11+
- Docker 20.10+
- Docker Compose 2.0+
- 2+ CPU cores
- 4+ GB RAM
- Домен с SSL сертификатом

### Установка на сервер

```bash
# 1. Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. Клонирование проекта
git clone https://github.com/yourusername/d3m-vpn-miniapp.git
cd d3m-vpn-miniapp

# 3. Настройка окружения
cp .env.example .env
nano .env

# 4. Настройка SSL
mkdir -p nginx/ssl
# Скопируйте сертификаты в nginx/ssl/
# fullchain.pem и privkey.pem

# 5. Запуск
docker compose up -d

# 6. Проверка
docker compose ps
```

### Настройка Nginx для продакшена

1. Получите SSL сертификат (Let's Encrypt):

```bash
apt install certbot
certbot certonly --standalone -d your-domain.com
```

2. Скопируйте сертификаты:

```bash
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/
```

3. Обновите `nginx/nginx.conf`:
   - Замените `server_name _` на ваш домен

4. Перезапустите:

```bash
docker compose restart nginx
```

---

## Troubleshooting

### Ошибки запуска

**Контейнер не запускается:**

```bash
# Проверьте логи
docker compose logs backend
docker compose logs frontend

# Проверьте статус
docker compose ps
```

**Ошибка подключения к БД:**

```bash
# Проверьте переменные окружения
docker compose exec backend env | grep DATABASE

# Проверьте доступность БД
docker compose exec backend ping db
```

**Ошибка аутентификации Telegram:**

- Проверьте `BOT_TOKEN` в `.env`
- Убедитесь, что время на сервере синхронизировано

**Ошибка RemnaWave API:**

```bash
# Проверьте подключение
docker compose exec backend curl -I https://api.remnawave.com

# Проверьте токен
docker compose exec backend env | grep REMNAWAVE
```

### Сброс состояния

```bash
# Полная очистка
docker compose down -v

# Удаление node_modules
rm -rf frontend/node_modules

# Пересборка
docker compose build --no-cache
docker compose up -d
```

---

## Поддержка

- **Telegram:** @your_support
- **Email:** support@yourdomain.com
- **GitHub Issues:** https://github.com/yourusername/d3m-vpn-miniapp/issues
