"""Зависимости API."""

from typing import AsyncGenerator, Optional

import redis.asyncio as redis
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.db.base import AsyncSessionLocal, get_db
from app.models.user import User
from app.services.device import DeviceService, get_device_service
from app.services.plan import PlanService, get_plan_service
from app.services.remnawave import RemnaWaveService, get_remnawave_service
from app.services.subscription import SubscriptionService, get_subscription_service
from app.services.user import UserService, get_user_service


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Получение Redis клиента."""
    client = redis.Redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    try:
        yield client
    finally:
        await client.close()


async def get_current_user(
    x_telegram_id: Optional[str] = Header(None, alias="X-Telegram-ID"),
    x_telegram_auth: Optional[str] = Header(None, alias="X-Telegram-Auth"),
) -> User:
    """Получение текущего пользователя из заголовков."""
    if not x_telegram_id:
        raise UnauthorizedException("Telegram ID не предоставлен")

    async for session in get_db():
        user_service = await get_user_service(session)
        user = await user_service.get_by_telegram_id(int(x_telegram_id))

        if not user:
            raise UnauthorizedException("Пользователь не найден")

        if user.is_blocked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь заблокирован",
            )

        return user

    raise UnauthorizedException("Не удалось получить сессию БД")


async def get_user_service_dep(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[UserService, None]:
    """Получение сервиса пользователя."""
    yield await get_user_service(session)


async def get_subscription_service_dep(
    session: AsyncSession = Depends(get_db),
    remnawave: RemnaWaveService = Depends(get_remnawave_service),
) -> AsyncGenerator[SubscriptionService, None]:
    """Получение сервиса подписок."""
    yield await get_subscription_service(session, remnawave)


async def get_device_service_dep(
    session: AsyncSession = Depends(get_db),
    remnawave: RemnaWaveService = Depends(get_remnawave_service),
) -> AsyncGenerator[DeviceService, None]:
    """Получение сервиса устройств."""
    yield await get_device_service(session, remnawave)


async def get_plan_service_dep(
    session: AsyncSession = Depends(get_db),
    remnawave: RemnaWaveService = Depends(get_remnawave_service),
) -> AsyncGenerator[PlanService, None]:
    """Получение сервиса планов."""
    yield await get_plan_service(session, remnawave)
