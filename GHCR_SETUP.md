# 🔗 Подключение к GitHub Container Registry

## 📦 Что было настроено

Этот проект теперь полностью интегрирован с **GitHub Container Registry (GHCR)** для автоматической сборки и публикации Docker образов.

---

## 📁 Созданные файлы

### GitHub Actions Workflows

| Файл | Назначение |
|------|------------|
| `.github/workflows/docker-build.yml` | Автоматическая сборка и публикация Docker образов |
| `.github/workflows/deploy.yml` | Автоматический деплой на сервер |

### Docker Compose файлы

| Файл | Назначение |
|------|------------|
| `docker-compose.yml` | Локальная сборка и запуск |
| `docker-compose.ghcr.yml` | Запуск с образами из GHCR |

### Скрипты

| Файл | Назначение |
|------|------------|
| `scripts/ghcr-login.sh` | Аутентификация в GitHub Container Registry |
| `Makefile.sh` | Обновлён с командами `ghcr-login` и `ghcr-up` |

### Dockerfile

| Файл | Назначение |
|------|------------|
| `nginx/Dockerfile` | Сборка образа Nginx для GHCR |

### Документация

| Файл | Назначение |
|------|------------|
| `GITHUB_PACKAGES.md` | Полная документация по GHCR интеграции |
| `GHCR_SETUP.md` | Эта инструкция |

---

## 🚀 Быстрый старт с GHCR

### Шаг 1: Получение GitHub Personal Access Token

1. Перейдите на https://github.com/settings/tokens
2. Нажмите **Generate new token (classic)**
3. Выберите scope'ы:
   - ✅ `read:packages`
   - ✅ `write:packages`
   - ✅ `repo`
4. Скопируйте токен (начинается с `ghp_`)

### Шаг 2: Аутентификация в GHCR

```bash
# Способ 1: Через скрипт
./scripts/ghcr-login.sh

# Способ 2: Через Makefile.sh
./Makefile.sh ghcr-login

# Способ 3: Вручную
echo YOUR_GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

### Шаг 3: Запуск с образами из GHCR

```bash
# Способ 1: Через docker-compose
docker compose -f docker-compose.ghcr.yml up -d

# Способ 2: Через Makefile.sh
./Makefile.sh ghcr-up
```

---

## 🔄 Автоматическая публикация образов

### При пуше в репозиторий

```
┌─────────────────┐
│   git push      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GitHub Actions │
│   (workflow)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build Docker   │
│     Images      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Push to GHCR   │
│ ghcr.io/owner/  │
│ d3m-vpn-miniapp │
└─────────────────┘
```

### Триггеры для сборки

| Событие | Ветка/Тег | Результат |
|---------|-----------|-----------|
| Push | `main` | `latest`, `main`, `sha-xxx` |
| Push | `develop` | `develop`, `sha-xxx` |
| Push tag | `v1.0.0` | `1.0.0`, `1.0`, `1`, `latest` |
| Pull Request | любая | `pr-{number}`, `sha-xxx` |

### Примеры тегов образов

```bash
# Для тега v1.2.3
ghcr.io/yourusername/d3m-vpn-miniapp/backend:1.2.3
ghcr.io/yourusername/d3m-vpn-miniapp/backend:1.2
ghcr.io/yourusername/d3m-vpn-miniapp/backend:1
ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest

# Для main ветки
ghcr.io/yourusername/d3m-vpn-miniapp/backend:main
ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest
ghcr.io/yourusername/d3m-vpn-miniapp/backend:sha-abc1234
```

---

## 🎯 Использование в production

### 1. Настройка сервера

```bash
# На сервере создайте .env файл
cat > /opt/d3m-vpn-miniapp/.env << EOF
# GHCR
REGISTRY=ghcr.io
GITHUB_OWNER=yourusername
IMAGE_TAG=v1.0.0

# Приложение
BOT_TOKEN=your-bot-token
REMNAWAVE_TOKEN=your-remnawave-token
DATABASE_PASSWORD=secure-password
REDIS_PASSWORD=secure-password
JWT_SECRET_KEY=secure-secret-key
EOF
```

### 2. Аутентификация на сервере

```bash
# На сервере выполните логин
echo $GHCR_TOKEN | docker login ghcr.io -u yourusername --password-stdin
```

### 3. Запуск через docker-compose

```bash
cd /opt/d3m-vpn-miniapp
docker compose -f docker-compose.ghcr.yml up -d
```

---

## 🛠️ CI/CD Pipeline

### Workflow 1: Build and Push

**Файл:** `.github/workflows/docker-build.yml`

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  build-backend:
    # Сборка и публикация backend образа
    # Multi-arch: linux/amd64, linux/arm64
    
  build-frontend:
    # Сборка и публикация frontend образа
    
  build-nginx:
    # Сборка и публикация nginx образа
```

### Workflow 2: Deploy

**Файл:** `.github/workflows/deploy.yml`

```yaml
name: Deploy to Production

on:
  push:
    tags: ['v*']
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        options: [production, staging]

jobs:
  deploy:
    # SSH деплой на сервер
    # Pull образов из GHCR
    # Перезапуск контейнеров
```

---

## 🔐 Настройка secrets для деплоя

В GitHub repository settings (**Settings → Secrets and variables → Actions**) добавьте:

### Repository Secrets

| Secret | Описание | Пример |
|--------|----------|--------|
| `SERVER_HOST` | IP или домен сервера | `192.168.1.100` или `vpn.example.com` |
| `SERVER_USER` | Пользователь SSH | `deploy` или `root` |
| `SSH_PRIVATE_KEY` | SSH ключ для доступа | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_PATH` | Путь к проекту на сервере | `/opt/d3m-vpn-miniapp` |

### Repository Variables

| Variable | Описание | Пример |
|----------|----------|--------|
| `APP_DOMAIN` | Домен приложения | `vpn.example.com` |

### Как создать SSH ключ для деплоя

```bash
# Генерация ключа
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_deploy

# Копирование публичного ключа на сервер
ssh-copy-id -i ~/.ssh/github_deploy.pub user@server

# Добавление приватного ключа в GitHub Secrets
cat ~/.ssh/github_deploy | gh secret set SSH_PRIVATE_KEY
```

---

## 📊 Мониторинг

### GitHub Actions

Проверка статуса сборок:
1. Перейдите в **Actions** tab репозитория
2. Выберите workflow
3. Просмотрите логи последнего запуска

### Docker логи на сервере

```bash
# Логи всех сервисов
docker compose -f docker-compose.ghcr.yml logs -f

# Логи конкретного сервиса
docker compose -f docker-compose.ghcr.yml logs backend
docker compose -f docker-compose.ghcr.yml logs frontend
```

---

## 🎮 Команды управления

### Локальная разработка

```bash
# Запуск с локальной сборкой
./Makefile.sh start

# Режим разработки
./Makefile.sh dev

# Просмотр логов
./Makefile.sh logs backend
```

### Production с GHCR

```bash
# Вход в GHCR
./Makefile.sh ghcr-login

# Запуск с GHCR образами
./Makefile.sh ghcr-up

# Перезапуск
docker compose -f docker-compose.ghcr.yml restart

# Обновление образов
docker compose -f docker-compose.ghcr.yml pull
docker compose -f docker-compose.ghcr.yml up -d
```

---

## 🔍 Troubleshooting

### Ошибка: "unauthorized: authentication required"

```bash
# Решение: залогиньтесь в GHCR
./scripts/ghcr-login.sh

# Или вручную
echo $GHCR_TOKEN | docker login ghcr.io -u $GITHUB_OWNER --password-stdin
```

### Ошибка: "image not found"

```bash
# Проверьте что образ опубликован
docker pull ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest

# Проверьте visibility пакета в GitHub
# Settings → Packages → d3m-vpn-miniapp → Visibility
```

### Ошибка деплоя: "Permission denied (publickey)"

```bash
# Проверьте SSH ключ
ssh -i ~/.ssh/github_deploy user@server

# Если не работает, пересоздайте ключ и добавьте в secrets
```

---

## 📈 Best Practices

### 1. Используйте конкретные теги в production

```yaml
# ❌ Плохо - может измениться
image: ghcr.io/owner/d3m-vpn-miniapp/backend:latest

# ✅ Хорошо - конкретная версия
image: ghcr.io/owner/d3m-vpn-miniapp/backend:v1.2.3
```

### 2. Автоматизируйте деплой тегами

```bash
# Создание релиза
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Автоматически запустит:
# 1. Сборку образов с тегами 1.0.0, 1.0, 1, latest
# 2. Деплой на production сервер
```

### 3. Регулярно обновляйте образы

```bash
# Скрипт для обновления
#!/bin/bash
cd /opt/d3m-vpn-miniapp
docker compose -f docker-compose.ghcr.yml pull
docker compose -f docker-compose.ghcr.yml up -d
docker image prune -f
```

---

## 🔗 Полезные ссылки

- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Buildx Docs](https://docs.docker.com/buildx/working-with-buildx/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GITHUB_PACKAGES.md](./GITHUB_PACKAGES.md) - Полная документация

---

## ✅ Чеклист готовности

- [ ] Получен GitHub Personal Access Token
- [ ] Выполнен вход в GHCR (`./scripts/ghcr-login.sh`)
- [ ] Проверен pull образов (`docker pull ghcr.io/...`)
- [ ] Настроен `.env` файл с переменными
- [ ] Добавлены secrets для деплоя (если нужно)
- [ ] Протестирован запуск (`./Makefile.sh ghcr-up`)

**Готово! 🎉**
