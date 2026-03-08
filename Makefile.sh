#!/bin/bash

# Скрипт для управления проектом D3M VPN MiniApp

set -e

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функции
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия .env файла
check_env() {
    if [ ! -f .env ]; then
        print_warning "Файл .env не найден. Копирую .env.example в .env"
        cp .env.example .env
        print_warning "Отредактируйте файл .env и заполните необходимыми значениями"
        exit 1
    fi
}

# Запуск проекта
start() {
    print_info "Запуск проекта..."
    check_env
    docker compose up -d
    print_info "Проект запущен!"
    print_info "Frontend: http://localhost"
    print_info "Backend API: http://localhost/api"
    print_info "API Docs: http://localhost/docs"
}

# Остановка проекта
stop() {
    print_info "Остановка проекта..."
    docker compose down
    print_info "Проект остановлен!"
}

# Перезапуск проекта
restart() {
    stop
    start
}

# Пересборка проекта
rebuild() {
    print_info "Пересборка проекта..."
    docker compose down
    docker compose build --no-cache
    docker compose up -d
    print_info "Проект пересобран и запущен!"
}

# Просмотр логов
logs() {
    local service=$1
    if [ -n "$service" ]; then
        docker compose logs -f "$service"
    else
        docker compose logs -f
    fi
}

# Очистка проекта
clean() {
    print_warning "Очистка проекта (удаление volumes)..."
    read -p "Вы уверены? Все данные будут удалены! (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        docker compose down -v
        print_info "Проект очищен!"
    else
        print_info "Очистка отменена"
    fi
}

# Установка зависимостей
install() {
    print_info "Установка зависимостей..."

    # Backend
    if [ -d "backend" ]; then
        print_info "Установка backend зависимостей..."
        cd backend
        pip install -r requirements.txt
        cd ..
    fi

    # Frontend
    if [ -d "frontend" ]; then
        print_info "Установка frontend зависимостей..."
        cd frontend
        npm install
        cd ..
    fi

    print_info "Зависимости установлены!"
}

# Запуск в режиме разработки
dev() {
    print_info "Запуск в режиме разработки..."
    check_env

    # Запуск только БД и Redis
    docker compose up -d db redis

    # Backend в режиме разработки
    cd backend
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    cd ..

    # Frontend в режиме разработки
    cd frontend
    npm run dev &
    cd ..

    print_info "Режим разработки запущен!"
    print_info "Frontend: http://localhost:5173"
    print_info "Backend API: http://localhost:8000"
    print_info "API Docs: http://localhost:8000/docs"
}

# Health check
health() {
    print_info "Проверка состояния сервисов..."
    docker compose ps
}

# Вывод справки
help() {
    echo "D3M VPN MiniApp - Управление проектом"
    echo ""
    echo "Использование: $0 <команда>"
    echo ""
    echo "Команды:"
    echo "  start       Запуск проекта"
    echo "  stop        Остановка проекта"
    echo "  restart     Перезапуск проекта"
    echo "  rebuild     Пересборка проекта"
    echo "  logs        Просмотр логов (можно указать сервис: logs backend)"
    echo "  clean       Очистка проекта (удаление volumes)"
    echo "  install     Установка зависимостей"
    echo "  dev         Запуск в режиме разработки"
    echo "  health      Проверка состояния сервисов"
    echo "  help        Вывод этой справки"
    echo ""
    echo "Примеры:"
    echo "  $0 start"
    echo "  $0 logs backend"
    echo "  $0 stop"
}

# Основная логика
case "${1:-help}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    rebuild)
        rebuild
        ;;
    logs)
        logs "$2"
        ;;
    clean)
        clean
        ;;
    install)
        install
        ;;
    dev)
        dev
        ;;
    health)
        health
        ;;
    help)
        help
        ;;
    *)
        print_error "Неизвестная команда: $1"
        help
        exit 1
        ;;
esac
