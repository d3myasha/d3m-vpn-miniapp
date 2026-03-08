# 🚀 Быстрая отправка в GitHub

## Что изменилось

`docker-compose.yml` теперь использует готовые образы из GitHub Container Registry:
- `ghcr.io/d3myasha/d3m-vpn-miniapp/backend:latest`
- `ghcr.io/d3myasha/d3m-vpn-miniapp/frontend:latest`
- `ghcr.io/d3myasha/d3m-vpn-miniapp/nginx:latest`

## Отправка изменений

### 1. Создайте Personal Access Token

Перейдите на https://github.com/settings/tokens

Нажмите **Generate new token (classic)**

Scope'ы:
- ✅ `repo`
- ✅ `workflow`

Скопируйте токен (начинается с `ghp_`)

### 2. Отправьте изменения

```bash
cd /home/demyasha/d3m-vpn-miniapp

# Установите токен (замените на ваш)
export GITHUB_TOKEN=ghp_yourtoken

# Отправьте изменения
git remote set-url origin https://$GITHUB_TOKEN@github.com/d3myasha/d3m-vpn-miniapp.git
git push origin main

# Верните оригинальный URL (опционально)
git remote set-url origin https://github.com/d3myasha/d3m-vpn-miniapp.git
```

Или используйте скрипт:

```bash
./scripts/push-to-github.sh
```

### 3. Дождитесь сборки

1. Перейдите на https://github.com/d3myasha/d3m-vpn-miniapp/actions
2. Дождитесь завершения "Build and Push Docker Images"
3. Образы будут опубликованы в GHCR

### 4. Запуск проекта

После успешной сборки:

```bash
cd /home/demyasha/d3m-vpn-miniapp

# Просто запустите docker-compose
docker compose up -d

# Docker автоматически скачает образы из GHCR
```

---

## ✅ Готово!

Теперь `docker compose up -d` будет скачивать готовые образы из GitHub, а не собирать их локально.
