"""API эндпоинты для подписок."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.deps import (
    get_current_user,
    get_subscription_service_dep,
    get_remnawave_service,
)
from app.core.exceptions import NotFoundException
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.user import User
from app.schemas import SubscriptionResponse
from app.services.subscription import SubscriptionService
from app.services.remnawave import RemnaWaveService

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.get("", response_model=List[SubscriptionResponse])
async def get_subscriptions(
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
) -> List[SubscriptionResponse]:
    """Получение всех подписок пользователя."""
    subscriptions = await subscription_service.get_by_user_telegram_id(
        current_user.telegram_id
    )
    return [SubscriptionResponse.model_validate(s) for s in subscriptions]


@router.get("/active", response_model=Optional[SubscriptionResponse])
async def get_active_subscription(
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
) -> Optional[SubscriptionResponse]:
    """Получение активной подписки."""
    subscription = await subscription_service.get_active_by_user(current_user.telegram_id)

    if not subscription:
        return None

    # Синхронизируем с RemnaWave
    await subscription_service.sync_with_remnawave(subscription)

    response = SubscriptionResponse.model_validate(subscription)
    response.days_left = subscription.days_left
    return response


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
) -> SubscriptionResponse:
    """Получение подписки по ID."""
    subscription = await subscription_service.get_by_id(subscription_id)

    if not subscription:
        raise NotFoundException("Подписка не найдена")

    # Проверяем принадлежность пользователю
    if subscription.user_telegram_id != current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    return SubscriptionResponse.model_validate(subscription)


@router.post("/{subscription_id}/renew", response_model=SubscriptionResponse)
async def renew_subscription(
    subscription_id: int,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
) -> SubscriptionResponse:
    """Продление подписки."""
    subscription = await subscription_service.get_by_id(subscription_id)

    if not subscription:
        raise NotFoundException("Подписка не найдена")

    if subscription.user_telegram_id != current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    subscription = await subscription_service.renew(subscription, days)
    logger.info(f"Пользователь {current_user.telegram_id} продлил подписку {subscription_id}")

    return SubscriptionResponse.model_validate(subscription)


@router.get("/{subscription_id}/traffic")
async def get_traffic_usage(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
) -> dict:
    """Получение использования трафика."""
    subscription = await subscription_service.get_by_id(subscription_id)

    if not subscription:
        raise NotFoundException("Подписка не найдена")

    if subscription.user_telegram_id != current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    usage = await subscription_service.get_traffic_usage(subscription)
    return usage
