# 📦 GitHub Packages Integration

## Настройка GitHub Container Registry (GHCR)

Этот проект использует **GitHub Container Registry** для хранения и распространения Docker образов.

### 📍 URL образов

| Образ | URL |
|-------|-----|
| Backend | `ghcr.io/yourusername/d3m-vpn-miniapp/backend` |
| Frontend | `ghcr.io/yourusername/d3m-vpn-miniapp/frontend` |
| Nginx | `ghcr.io/yourusername/d3m-vpn-miniapp/nginx` |

Замените `yourusername` на ваш GitHub username или organization.

---

## 🚀 Автоматическая публикация образов

### Триггеры для сборки

Сборка и публикация образов происходит автоматически при:

1. **Push в ветку `main`** - создаются образы с тегом `latest`
2. **Push в ветку `develop`** - создаются образы с тегом `develop`
3. **Создание тега** (например, `v1.0.0`) - создаются образы с тегом версии
4. **Pull Request** - создаются тестовые образы

### Теги образов

Автоматически создаваемые теги:

```
# Для тега v1.2.3
ghcr.io/owner/d3m-vpn-miniapp/backend:1.2.3
ghcr.io/owner/d3m-vpn-miniapp/backend:1.2
ghcr.io/owner/d3m-vpn-miniapp/backend:1
ghcr.io/owner/d3m-vpn-miniapp/backend:sha-abc123

# Для main ветки
ghcr.io/owner/d3m-vpn-miniapp/backend:main
ghcr.io/owner/d3m-vpn-miniapp/backend:latest
ghcr.io/owner/d3m-vpn-miniapp/backend:sha-abc123

# Для develop ветки
ghcr.io/owner/d3m-vpn-miniapp/backend:develop
ghcr.io/owner/d3m-vpn-miniapp/backend:sha-abc123
```

---

## 🔐 Настройка доступа

### 1. Токен для GHCR

Для использования образов из GHCR создайте Personal Access Token:

1. Перейдите в **GitHub Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Нажмите **Generate new token (classic)**
3. Выберите scopes:
   - ✅ `read:packages` - для скачивания образов
   - ✅ `write:packages` - для публикации образов (для CI/CD)
   - ✅ `repo` - полный доступ к репозиторию
4. Скопируйте токен (начинается с `ghp_`)

### 2. Аутентификация в GHCR

```bash
# Логин в GHCR
echo $GHCR_TOKEN | docker login ghcr.io -u yourusername --password-stdin
```

### 3. Docker Compose аутентификация

Создайте файл `~/.docker/config.json`:

```json
{
  "auths": {
    "ghcr.io": {
      "auth": "base64_encoded_credentials"
    }
  }
}
```

Или используйте Docker credential helper:

```bash
# Установка docker-credential-pass
apt install pass

# Создание credentials
echo "ghcr.io" | docker-credential-pass init
echo -e "yourusername\nghp_yourtoken" | docker-credential-pass insert ghcr.io
```

---

## 📥 Использование образов

### Вариант 1: Docker Compose с GHCR

```bash
# Копируем файл для GHCR
cp docker-compose.ghcr.yml docker-compose.yml

# Настраиваем переменные окружения
cat > .env << EOF
REGISTRY=ghcr.io
GITHUB_OWNER=yourusername
IMAGE_TAG=latest

# Остальные переменные...
BOT_TOKEN=your-bot-token
REMNAWAVE_TOKEN=your-remnawave-token
DATABASE_PASSWORD=secure-password
EOF

# Запускаем
docker compose up -d
```

### Вариант 2: Ручной запуск

```bash
# Pull образов
docker pull ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest
docker pull ghcr.io/yourusername/d3m-vpn-miniapp/frontend:latest
docker pull ghcr.io/yourusername/d3m-vpn-miniapp/nginx:latest

# Запуск backend
docker run -d \
  --name d3mvpn-backend \
  --env-file .env \
  --network d3mvpn-network \
  ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest

# Запуск frontend
docker run -d \
  --name d3mvpn-frontend \
  --env-file .env \
  --network d3mvpn-network \
  ghcr.io/yourusername/d3m-vpn-miniapp/frontend:latest

# Запуск nginx
docker run -d \
  --name d3mvpn-nginx \
  -p 80:80 \
  -p 443:443 \
  -v ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v ./nginx/ssl:/etc/nginx/ssl:ro \
  --network d3mvpn-network \
  ghcr.io/yourusername/d3m-vpn-miniapp/nginx:latest
```

---

## 🔧 CI/CD Pipeline

### Workflow файлы

Проект содержит два workflow файла:

#### 1. `docker-build.yml` - Сборка и публикация

```yaml
# Автоматическая сборка при:
# - Push в main/develop
# - Создании тега
# - Pull Request

# Публикует образы в:
# ghcr.io/owner/d3m-vpn-miniapp/{backend,frontend,nginx}
```

#### 2. `deploy.yml` - Деплой на сервер

```yaml
# Деплой при:
# - Создании тега (v*)
# - Ручном запуске (workflow_dispatch)

# Требования:
# - SSH доступ к серверу
# - Secrets: SERVER_HOST, SERVER_USER, SSH_PRIVATE_KEY
```

### Настройка secrets для деплоя

В GitHub repository settings добавьте:

| Secret | Описание | Пример |
|--------|----------|--------|
| `SERVER_HOST` | IP или домен сервера | `192.168.1.100` |
| `SERVER_USER` | Пользователь SSH | `deploy` |
| `SSH_PRIVATE_KEY` | SSH ключ для доступа | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_PATH` | Путь к проекту на сервере | `/opt/d3m-vpn-miniapp` |

### Настройка variables для деплоя

| Variable | Описание | Пример |
|----------|----------|--------|
| `APP_DOMAIN` | Домен приложения | `vpn.example.com` |

---

## 🏷️ Версионирование

### Семантическое версионирование

Проект использует семантическое версионирование:

```
v{MAJOR}.{MINOR}.{PATCH}

Примеры:
v1.0.0  - Первый релиз
v1.2.3  - Патч релиз
v2.0.0  - Мажорный релиз
```

### Создание релиза

```bash
# Создаём тег
git tag -a v1.0.0 -m "Release version 1.0.0"

# Пушим тег
git push origin v1.0.0

# Или создаём релиз через GitHub UI
```

После пуша тега автоматически:
1. Соберутся Docker образы с тегами версии
2. Запустится деплой на production сервер

---

## 🔍 Мониторинг и логи

### GitHub Actions

Проверка статуса сборок:
- Перейдите в **Actions** tab вашего репозитория
- Выберите workflow (Build and Push / Deploy)
- Просмотрите логи последнего запуска

### Docker логи

```bash
# Логи всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f backend
docker compose logs -f frontend
```

---

## 🛠️ Troubleshooting

### Ошибка: "unauthorized: authentication required"

```bash
# Решение: залогиньтесь в GHCR
echo $GHCR_TOKEN | docker login ghcr.io -u yourusername --password-stdin
```

### Ошибка: "image not found"

```bash
# Проверьте правильность owner в IMAGE_PREFIX
# Убедитесь что образ опубликован:
docker pull ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest
```

### Ошибка деплоя: "Permission denied (publickey)"

```bash
# Проверьте SSH ключ:
# 1. Сгенерируйте новый ключ
ssh-keygen -t ed25519 -C "github-actions"

# 2. Добавьте публичный ключ на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# 3. Добавьте приватный ключ в GitHub Secrets
cat ~/.ssh/id_ed25519 | gh secret set SSH_PRIVATE_KEY
```

### Ошибка: "container already exists"

```bash
# Остановите и удалите старые контейнеры
docker compose -f docker-compose.ghcr.yml down
docker compose -f docker-compose.ghcr.yml up -d
```

---

## 📊 Package Settings

### Видимость пакетов

По умолчанию пакеты в GHCR имеют ту же видимость, что и репозиторий:

- **Публичный репозиторий** → Публичные пакеты
- **Приватный репозиторий** → Приватные пакеты

Изменить видимость можно в **Package Settings**:
1. Перейдите на страницу пакета
2. Нажмите **Settings**
3. Измените **Visibility**

### Управление версиями

Для удаления старых версий:

```bash
# Через GitHub CLI
gh api \
  -H "Accept: application/vnd.github+json" \
  /user/packages/container/d3m-vpn-miniapp%2Fbackend/versions \
  | jq '.[] | select(.name | contains("sha")) | .id' \
  | xargs -I {} gh api -X DELETE /user/packages/container/d3m-vpn-miniapp%2Fbackend/versions/{}
```

---

## 📈 Best Practices

### 1. Используйте specific tags

```yaml
# ❌ Плохо - может измениться
image: ghcr.io/owner/d3m-vpn-miniapp/backend:latest

# ✅ Хорошо - конкретная версия
image: ghcr.io/owner/d3m-vpn-miniapp/backend:v1.2.3
```

### 2. Обновляйте образы регулярно

```bash
# Скрипт для обновления
#!/bin/bash
docker compose -f docker-compose.ghcr.yml pull
docker compose -f docker-compose.ghcr.yml up -d
docker image prune -f
```

### 3. Используйте multi-arch образы

Workflow автоматически собирает образы для:
- `linux/amd64` (стандартные серверы)
- `linux/arm64` (Raspberry Pi, M1/M2 Mac)

### 4. Кэшируйте слои

GitHub Actions использует GitHub Cache для ускорения сборок.

---

## 🔗 Полезные ссылки

- [GitHub Container Registry Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Buildx Documentation](https://docs.docker.com/buildx/working-with-buildx/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
