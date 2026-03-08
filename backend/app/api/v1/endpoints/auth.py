"""API эндпоинты для аутентификации."""

import hashlib
import hmac
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from urllib.parse import parse_qs

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from loguru import logger

from app.api.deps import get_current_user, get_redis, get_user_service_dep
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.models.user import User
from app.schemas import TokenResponse, UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def verify_telegram_auth(
    init_data: Dict[str, Any],
    token: str,
) -> bool:
    """Проверка подлинности данных Telegram."""
    # Проверяем время (данные действительны 24 часа)
    auth_date = datetime.fromtimestamp(init_data["auth_date"], tz=timezone.utc)
    if datetime.now(timezone.utc) - auth_date > timedelta(hours=24):
        return False

    # Проверяем хэш
    received_hash = init_data.pop("hash", None)
    if not received_hash:
        return False

    # Сортируем данные и создаём data_check_string
    data_check_arr = []
    for key, value in sorted(init_data.items()):
        data_check_arr.append(f"{key}={value}")
    data_check_string = "\n".join(data_check_arr)

    # Создаём хэш
    secret_key = hmac.new(
        b"WebAppData",
        token.encode(),
        hashlib.sha256,
    ).digest()

    computed_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(received_hash, computed_hash)


@router.post("/init")
async def init_auth(
    init_data: Dict[str, Any],
    redis_client: redis.Redis = Depends(get_redis),
    user_service: UserService = Depends(get_user_service_dep),
) -> TokenResponse:
    """
    Инициализация аутентификации через Telegram.

    Принимает данные из Telegram WebApp initData.
    """
    # Проверяем подлинность данных Telegram
    if not verify_telegram_auth(init_data.copy(), settings.bot_token):
        raise UnauthorizedException("Неверные данные аутентификации Telegram")

    # Получаем данные пользователя
    telegram_user = init_data.get("user", {})
    telegram_id = int(telegram_user.get("id"))
    username = telegram_user.get("username")
    first_name = telegram_user.get("first_name", "")
    last_name = telegram_user.get("last_name", "")
    name = f"{first_name} {last_name}".strip() or f"User {telegram_id}"

    # Проверяем реферальный параметр
    start_param = init_data.get("start_param")

    # Ищем существующего пользователя
    user = await user_service.get_by_telegram_id(telegram_id)

    if not user:
        # Создаём нового пользователя
        import secrets

        referral_code = secrets.token_urlsafe(8)

        # Проверяем реферала
        referred_by = None
        if start_param and start_param.startswith("ref_"):
            ref_code = start_param[4:]
            async for session_dep in user_service.session:
                from sqlalchemy import select
                from app.models.user import User as UserModel

                result = await session_dep.execute(
                    select(UserModel).where(UserModel.referral_code == ref_code)
                )
                referred_by = result.scalar_one_or_none()

        user_data = UserCreate(
            telegram_id=telegram_id,
            username=username,
            name=name,
            referral_code=referral_code,
            language="ru",
        )
        user = await user_service.create(
            user_data,
            referred_by_id=referred_by.id if referred_by else None,
        )
        logger.info(f"Создан новый пользователь: {user.telegram_id}")
    else:
        # Обновляем данные пользователя
        from app.schemas import UserUpdate

        update_data = UserUpdate(username=username, name=name)
        user = await user_service.update(user, update_data)

    # Генерируем JWT токен
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    to_encode = {
        "sub": str(user.id),
        "telegram_id": user.telegram_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    # Сохраняем в Redis для быстрого доступа
    await redis_client.setex(
        f"user:session:{user.telegram_id}",
        timedelta(hours=1),
        str(user.id),
    )

    return TokenResponse(access_token=encoded_jwt)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Получение текущего пользователя."""
    return UserResponse.model_validate(current_user)


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    redis_client: redis.Redis = Depends(get_redis),
) -> Dict[str, bool]:
    """Выход из системы."""
    await redis_client.delete(f"user:session:{current_user.telegram_id}")
    return {"success": True}
