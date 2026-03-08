# 🚀 Быстрая настройка GHCR

## Способ 1: Через скрипт (рекомендуется)

```bash
./scripts/ghcr-login.sh
```

Скрипт запросит:
1. GitHub Personal Access Token
2. GitHub username

## Способ 2: Через переменные окружения

```bash
# Установите переменные
export GITHUB_OWNER=yourusername
export GHCR_TOKEN=ghp_yourtoken

# Выполните вход
echo $GHCR_TOKEN | docker login ghcr.io -u $GITHUB_OWNER --password-stdin

# Или через Makefile.sh
./Makefile.sh ghcr-login
```

## Способ 3: Через .env файл

```bash
# Скопируйте .env.example
cp .env.example .env

# Отредактируйте .env
nano .env

# Добавьте:
REGISTRY=ghcr.io
GITHUB_OWNER=yourusername
GHCR_TOKEN=ghp_yourtoken
IMAGE_TAG=latest

# Затем выполните вход
./scripts/ghcr-login.sh
```

---

## 🔑 Получение GitHub Personal Access Token

1. Перейдите на https://github.com/settings/tokens
2. Нажмите **Generate new token (classic)**
3. Дайте название токену (например, "GHCR d3m-vpn-miniapp")
4. Выберите scope'ы:
   - ✅ `read:packages`
   - ✅ `write:packages`
   - ✅ `repo` (полный доступ к репозиторию)
5. Нажмите **Generate token**
6. **Скопируйте токен** (начинается с `ghp_`)

⚠️ **Важно:** Сохраните токен в безопасном месте! После закрытия страницы вы не сможете его увидеть снова.

---

## ✅ Проверка

После успешного входа попробуйте pull образа:

```bash
# Замените yourusername на ваш GitHub username
docker pull ghcr.io/yourusername/d3m-vpn-miniapp/backend:latest
```

Или запустите весь проект:

```bash
./Makefile.sh ghcr-up
```

---

## 📝 Примечания

- Токен хранится в `~/.docker/config.json`
- Для обновления образов: `docker compose -f docker-compose.ghcr.yml pull`
- Для выхода: `docker logout ghcr.io`
