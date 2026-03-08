"""Главный файл приложения FastAPI."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppException, BadRequestException, NotFoundException
from app.db.init import init_db
from app.services.remnawave import remnawave_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Управление жизненным циклом приложения."""
    # Startup
    logger.info("Запуск приложения...")

    # Инициализация базы данных
    await init_db()
    logger.info("База данных инициализирована")

    yield

    # Shutdown
    logger.info("Остановка приложения...")
    await remnawave_service.close()


# Создание приложения
app = FastAPI(
    title="D3M VPN MiniApp API",
    description="API для управления VPN подписками через Telegram MiniApp",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(api_router, prefix="/api/v1")


# Обработчики исключений
@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    """Обработчик исключений приложения."""
    return {
        "success": False,
        "error": exc.detail,
    }, exc.status_code


@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request, exc: BadRequestException):
    """Обработчик ошибок неверного запроса."""
    return {
        "success": False,
        "error": exc.detail,
    }, 400


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc: NotFoundException):
    """Обработчик ошибок не найдено."""
    return {
        "success": False,
        "error": exc.detail,
    }, 404


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Проверка здоровья приложения."""
    return {"status": "healthy", "version": "1.0.0"}


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Корневой эндпоинт."""
    return {
        "message": "D3M VPN MiniApp API",
        "docs": "/docs",
        "health": "/health",
    }
