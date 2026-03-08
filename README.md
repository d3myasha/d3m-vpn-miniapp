# D3M VPN MiniApp

Telegram MiniApp для управления VPN-подписками на основе бота **RemnaShop**.

## 🏗️ Архитектура

```
┌─────────────────┐
│  Telegram Web   │
│   (MiniApp)     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   Frontend      │
│  (React +       │
│   Bootstrap)    │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│   Backend       │
│  (FastAPI)      │
└────────┬────────┘
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
┌────────┐ ┌────────┐ ┌─────────┐
│Postgres│ │ Redis  │ │RemnaWave│
│   DB   │ │ (cache)│ │  API    │
└────────┘ └────────┘ └─────────┘
```

## 📁 Структура проекта

```
d3m-vpn-miniapp/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── auth.py        # Аутентификация
│   │   │   │   │   ├── user.py        # Пользователи
│   │   │   │   │   ├── subscription.py # Подписки
│   │   │   │   │   ├── device.py      # Устройства
│   │   │   │   │   ├── plan.py        # Тарифы
│   │   │   │   │   ├── promocode.py   # Промокоды
│   │   │   │   │   ├── payment.py     # Платежи
│   │   │   │   │   └── referral.py    # Рефералы
│   │   │   │   └── router.py
│   │   │   └── deps.py    # Зависимости
│   │   ├── core/
│   │   │   ├── config.py  # Конфигурация
│   │   │   ├── security.py # Безопасность
│   │   │   └── exceptions.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── subscription.py
│   │   │   ├── transaction.py
│   │   │   ├── plan.py
│   │   │   ├── promocode.py
│   │   │   ├── referral.py
│   │   │   └── device.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── subscription.py
│   │   │   ├── transaction.py
│   │   │   ├── plan.py
│   │   │   ├── promocode.py
│   │   │   ├── referral.py
│   │   │   └── device.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── subscription.py
│   │   │   ├── remnawave.py  # RemnaWave API client
│   │   │   ├── payment.py
│   │   │   ├── promocode.py
│   │   │   └── notification.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── api/           # API client
│   │   │   └── index.ts
│   │   ├── components/    # React компоненты
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Loader.tsx
│   │   │   │   └── Error.tsx
│   │   │   ├── subscription/
│   │   │   │   ├── SubscriptionCard.tsx
│   │   │   │   ├── SubscriptionStatus.tsx
│   │   │   │   └── TrafficUsage.tsx
│   │   │   ├── device/
│   │   │   │   ├── DeviceList.tsx
│   │   │   │   └── DeviceItem.tsx
│   │   │   ├── plan/
│   │   │   │   ├── PlanCard.tsx
│   │   │   │   └── PlanList.tsx
│   │   │   ├── payment/
│   │   │   │   ├── PaymentMethod.tsx
│   │   │   │   └── PaymentForm.tsx
│   │   │   └── promocode/
│   │   │       └── PromocodeInput.tsx
│   │   ├── hooks/         # Custom hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useSubscription.ts
│   │   │   └── useDevices.ts
│   │   ├── pages/         # Страницы
│   │   │   ├── Home.tsx
│   │   │   ├── Subscription.tsx
│   │   │   ├── Devices.tsx
│   │   │   ├── Plans.tsx
│   │   │   ├── Payment.tsx
│   │   │   ├── Profile.tsx
│   │   │   └── Referral.tsx
│   │   ├── store/         # State management
│   │   │   └── index.ts
│   │   ├── types/         # TypeScript types
│   │   │   └── index.ts
│   │   ├── utils/         # Utilities
│   │   │   └── format.ts
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── index.css
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/yourusername/d3m-vpn-miniapp.git
cd d3m-vpn-miniapp
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
# Отредактируйте .env и заполните необходимыми значениями
```

### 3. Запуск через Docker Compose

**Вариант A: Локальная сборка**

```bash
docker compose up -d
```

**Вариант B: Использование образов из GitHub Container Registry**

```bash
# Вход в GHCR
./scripts/ghcr-login.sh

# Или через Makefile.sh
./Makefile.sh ghcr-login

# Запуск с GHCR образами
docker compose -f docker-compose.ghcr.yml up -d

# Или через Makefile.sh
./Makefile.sh ghcr-up
```

### 4. Проверка статуса

```bash
docker compose ps
```

## ⚙️ Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `APP_DOMAIN` | Домен приложения | `vpn.example.com` |
| `BOT_TOKEN` | Токен Telegram бота | `123456:ABC-DEF1234...` |
| `BOT_SECRET_TOKEN` | Секрет для вебхуков | `your-secret-token` |
| `REMNAWAVE_HOST` | Хост RemnaWave API | `api.remnawave.com` |
| `REMNAWAVE_TOKEN` | Токен RemnaWave | `your-remnawave-token` |
| `DATABASE_URL` | URL подключения к БД | `postgresql://user:pass@db:5432/d3mvpn` |
| `REDIS_URL` | URL подключения к Redis | `redis://redis:6379` |
| `SECRET_KEY` | Секретный ключ для JWT | `your-secret-key` |

## 📊 Функционал MiniApp

### Пользовательские функции

- **👤 Профиль** - просмотр и редактирование профиля
- **📦 Подписка** - статус, продление, управление
- **📱 Устройства** - добавление/удаление устройств
- **💳 Планы** - выбор и покупка тарифа
- **🎟️ Промокоды** - активация промокодов
- **💰 Платежи** - оплата подписки
- **👥 Рефералы** - реферальная программа
- **📊 Статистика** - использование трафика

### Административные функции (для админов)

- Управление пользователями
- Управление подписками
- Просмотр транзакций
- Настройка тарифов

## 🔌 API Endpoints

### Authentication

- `POST /api/v1/auth/init` - Инициализация сессии из Telegram
- `GET /api/v1/auth/me` - Получение текущего пользователя

### Users

- `GET /api/v1/users/me` - Профиль пользователя
- `PUT /api/v1/users/me` - Обновление профиля

### Subscriptions

- `GET /api/v1/subscriptions` - Список подписок
- `GET /api/v1/subscriptions/active` - Активная подписка
- `POST /api/v1/subscriptions/renew` - Продление подписки

### Devices

- `GET /api/v1/devices` - Список устройств
- `POST /api/v1/devices` - Добавить устройство
- `DELETE /api/v1/devices/{id}` - Удалить устройство

### Plans

- `GET /api/v1/plans` - Список тарифов
- `GET /api/v1/plans/{id}` - Детали тарифа

### Payments

- `POST /api/v1/payments/create` - Создание платежа
- `GET /api/v1/payments/{id}` - Статус платежа

### Promocodes

- `POST /api/v1/promocodes/activate` - Активация промокода

### Referrals

- `GET /api/v1/referrals` - Реферальная статистика
- `GET /api/v1/referrals/code` - Реферальный код

## 🛠️ Технологии

### Backend

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - база данных
- **Redis** - кэш и сессии
- **Pydantic** - валидация данных
- **python-jose** - JWT токены

### Frontend

- **React 18** - UI библиотека
- **TypeScript** - типизация
- **Bootstrap 5** - стилизация
- **React Router** - роутинг
- **Zustand** - state management
- **Axios** - HTTP клиент
- **Vite** - сборщик

### DevOps

- **Docker** - контейнеризация
- **Docker Compose** - оркестрация
- **Nginx** - reverse proxy (опционально)

## 📝 Лицензия

MIT
