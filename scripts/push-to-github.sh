#!/bin/bash

# Скрипт для отправки изменений в GitHub

set -e

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

cd /home/demyasha/d3m-vpn-miniapp

# Проверка изменений
if git status --porcelain | grep -q "^M"; then
    print_info "Есть незакоммиченные изменения. Коммитим..."
    git add -A
    git commit -m "fix: TypeScript compilation errors"
fi

# Получение токена
if [ -z "$GITHUB_TOKEN" ]; then
    print_warning "GITHUB_TOKEN не установлен"
    print_info "Создайте токен на: https://github.com/settings/tokens"
    print_info "Необходимые scope: repo, workflow"
    echo ""
    read -p "Введите ваш GitHub Personal Access Token: " -s GITHUB_TOKEN
    echo ""
fi

if [ -z "$GITHUB_TOKEN" ]; then
    print_error "Токен не предоставлен"
    exit 1
fi

# Отправка изменений
print_info "Отправка изменений в GitHub..."

# Временная смена URL remote
git remote set-url origin https://$GITHUB_TOKEN@github.com/d3myasha/d3m-vpn-miniapp.git

# Пуш
if git push origin main; then
    print_info "✅ Изменения успешно отправлены!"
    print_info "GitHub Actions автоматически перезапустит сборку..."
else
    print_error "❌ Ошибка отправки изменений"
    exit 1
fi

# Возврат оригинального URL
git remote set-url origin https://github.com/d3myasha/d3m-vpn-miniapp.git

print_info "Готово! Проверьте статус сборки на GitHub Actions"
