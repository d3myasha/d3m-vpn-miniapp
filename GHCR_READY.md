# 🔗 GitHub Container Registry - Настройка завершена!

## ✅ Что было сделано

### 1. Созданы GitHub Actions Workflows

**`.github/workflows/docker-build.yml`**
- Автоматическая сборка Docker образов при:
  - Push в ветку `main` → тег `latest`
  - Push в ветку `develop` → тег `develop`
  - Создании тега `v*` → теги версии
  - Pull Request → тестовые образы
- Публикация в GHCR: `ghcr.io/owner/d3m-vpn-miniapp/{backend,frontend,nginx}`
- Multi-arch сборка: `linux/amd64`, `linux/arm64`

**`.github/workflows/deploy.yml`**
- Автоматический деплой при создании тега
- Ручной запуск через workflow_dispatch
- SSH деплой на сервер
- Health check после деплоя

### 2. Docker Compose файлы

**`docker-compose.ghcr.yml`**
- Конфигурация для запуска с образами из GHCR
- Переменные окружения для настройки registry
- Pull policy: `always` для автоматического обновления

### 3. Скрипты

**`scripts/ghcr-login.sh`**
- Интерактивная аутентификация в GHCR
- Запрос токена и username
- Автоматическое создание `.env` файла

**`Makefile.sh`** (обновлён)
- `./Makefile.sh ghcr-login` - вход в GHCR
- `./Makefile.sh ghcr-up` - запуск с GHCR образами

### 4. Документация

- **`QUICK_START_GHCR.md`** - быстрый старт (3 способа)
- **`GHCR_SETUP.md`** - подробная инструкция
- **`GITHUB_PACKAGES.md`** - полная документация по GHCR

---

## 🚀 Использование

### Вариант 1: Интерактивный (рекомендуется)

```bash
# 1. Запустите скрипт
./scripts/ghcr-login.sh

# 2. Введите GitHub Personal Access Token
# 3. Введите GitHub username

# 4. Запустите проект
./Makefile.sh ghcr-up
```

### Вариант 2: Через переменные окружения

```bash
# Установите переменные
export GITHUB_OWNER=yourusername
export GHCR_TOKEN=ghp_yourtoken

# Выполните вход
echo $GHCR_TOKEN | docker login ghcr.io -u $GITHUB_OWNER --password-stdin

# Запустите проект
docker compose -f docker-compose.ghcr.yml up -d
```

### Вариант 3: Через .env файл

```bash
# Скопируйте шаблон
cp .env.example .env

# Отредактируйте .env
nano .env

# Добавьте:
REGISTRY=ghcr.io
GITHUB_OWNER=yourusername
GHCR_TOKEN=ghp_yourtoken
IMAGE_TAG=latest

# Запустите скрипт
./scripts/ghcr-login.sh

# Или сразу запустите проект
./Makefile.sh ghcr-up
```

---

## 📦 URL образов

После публикации образы будут доступны по URL:

```
ghcr.io/{GITHUB_OWNER}/d3m-vpn-miniapp/backend:{TAG}
ghcr.io/{GITHUB_OWNER}/d3m-vpn-miniapp/frontend:{TAG}
ghcr.io/{GITHUB_OWNER}/d3m-vpn-miniapp/nginx:{TAG}
```

### Примеры тегов

| Событие | Теги |
|---------|------|
| Push в `main` | `main`, `latest`, `sha-abc123` |
| Push в `develop` | `develop`, `sha-abc123` |
| Тег `v1.2.3` | `1.2.3`, `1.2`, `1`, `latest` |
| Pull Request | `pr-123`, `sha-abc123` |

---

## 🔑 Получение токена

1. Перейдите на https://github.com/settings/tokens
2. Нажмите **Generate new token (classic)**
3. Выберите scope'ы:
   - ✅ `read:packages` - для скачивания образов
   - ✅ `write:packages` - для публикации образов
   - ✅ `repo` - для доступа к репозиторию
4. Скопируйте токен (начинается с `ghp_`)

---

## 🧪 Проверка

### 1. Проверка входа в GHCR

```bash
docker login ghcr.io
# Должно вывести: Login Succeeded
```

### 2. Pull тестового образа

```bash
# Замените yourusername на ваш GitHub username
docker pull ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest
```

### 3. Запуск проекта

```bash
./Makefile.sh ghcr-up

# Проверка статуса
docker compose -f docker-compose.ghcr.yml ps
```

---

## 🔄 Автоматическая публикация

После настройки workflows образы будут публиковаться автоматически:

```bash
# 1. Создайте коммит
git add .
git commit -m "feat: добавлена новая функция"

# 2. Создайте тег
git tag -a v1.0.0 -m "Release version 1.0.0"

# 3. Отправьте в репозиторий
git push origin v1.0.0

# 4. GitHub Actions автоматически:
#    - Соберёт образы
#    - Опубликует в GHCR
#    - Задеплоит на сервер (если настроен)
```

---

## 🛠️ Настройка деплоя (опционально)

Для автоматического деплоя добавьте secrets в GitHub:

**Settings → Secrets and variables → Actions → New repository secret**

| Secret | Пример |
|--------|--------|
| `SERVER_HOST` | `192.168.1.100` |
| `SERVER_USER` | `deploy` |
| `SSH_PRIVATE_KEY` | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `DEPLOY_PATH` | `/opt/d3m-vpn-miniapp` |

**Settings → Variables → Actions → New repository variable**

| Variable | Пример |
|----------|--------|
| `APP_DOMAIN` | `vpn.example.com` |

---

## 📚 Документация

- **QUICK_START_GHCR.md** - 3 способа аутентификации
- **GHCR_SETUP.md** - подробная инструкция по настройке
- **GITHUB_PACKAGES.md** - документация по GitHub Packages
- **README.md** - общая документация проекта

---

## ⚠️ Troubleshooting

### Ошибка: "unauthorized: authentication required"

```bash
# Решение: перезалогиньтесь
docker logout ghcr.io
./scripts/ghcr-login.sh
```

### Ошибка: "denied: insufficient_permissions"

- Проверьте что токен имеет scope `read:packages`
- Убедитесь что репозиторий публичный или токен имеет доступ к приватному

### Ошибка: "image not found"

- Проверьте правильность `GITHUB_OWNER` в `.env`
- Убедитесь что образ опубликован в GHCR

---

## ✅ Чеклист

- [ ] Получен GitHub Personal Access Token
- [ ] Скрипт `./scripts/ghcr-login.sh` выполнен успешно
- [ ] `docker login ghcr.io` возвращает "Login Succeeded"
- [ ] `docker pull ghcr.io/.../backend:latest` работает
- [ ] Проект запускается через `./Makefile.sh ghcr-up`

**Готово! 🎉**
