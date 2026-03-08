#!/bin/bash

# Скрипт для аутентификации в GitHub Container Registry

set -e

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия токена
if [ -z "$GHCR_TOKEN" ]; then
    if [ -f .env ]; then
        source .env
    fi
fi

if [ -z "$GHCR_TOKEN" ]; then
    print_warning "GHCR_TOKEN не найден в окружении или .env файле"
    print_info "Получите токен на: https://github.com/settings/tokens"
    print_info "Необходимые scope: read:packages, write:packages"
    echo ""
    read -p "Введите ваш GitHub Personal Access Token: " -s GHCR_TOKEN
    echo ""
fi

# Определение username из токена
if [ -z "$GITHUB_OWNER" ]; then
    print_info "Определяем GitHub username..."
    GITHUB_OWNER=$(curl -s -H "Authorization: token $GHCR_TOKEN" \
      https://api.github.com/user | grep -o '"login":"[^"]*"' | cut -d'"' -f4)

    if [ -z "$GITHUB_OWNER" ]; then
        print_error "Не удалось определить GitHub username"
        exit 1
    fi

    print_info "GitHub username: $GITHUB_OWNER"
fi

# Логин в GHCR
print_info "Выполняем вход в GitHub Container Registry..."

echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GITHUB_OWNER" --password-stdin

if [ $? -eq 0 ]; then
    print_info "✅ Успешный вход в GHCR!"
    print_info "Теперь вы можете:"
    echo ""
    echo "  # Pull образов:"
    echo "  docker pull ghcr.io/$GITHUB_OWNER/d3m-vpn-miniapp/backend:latest"
    echo "  docker pull ghcr.io/$GITHUB_OWNER/d3m-vpn-miniapp/frontend:latest"
    echo "  docker pull ghcr.io/$GITHUB_OWNER/d3m-vpn-miniapp/nginx:latest"
    echo ""
    echo "  # Или запустить через docker-compose:"
    echo "  docker compose -f docker-compose.ghcr.yml up -d"
    echo ""

    # Сохраняем в .env если не существует
    if [ ! -f .env ]; then
        print_info "Создаём файл .env..."
        cat > .env << EOF
# GitHub Container Registry
REGISTRY=ghcr.io
GITHUB_OWNER=$GITHUB_OWNER
IMAGE_TAG=latest
GHCR_TOKEN=$GHCR_TOKEN

# Остальные переменные...
BOT_TOKEN=your-bot-token
REMNAWAVE_TOKEN=your-remnawave-token
DATABASE_PASSWORD=change-me
REDIS_PASSWORD=change-me
JWT_SECRET_KEY=change-me
EOF
        print_warning "Не забудьте заполнить остальные переменные в .env!"
    fi
else
    print_error "❌ Ошибка входа в GHCR"
    exit 1
fi
