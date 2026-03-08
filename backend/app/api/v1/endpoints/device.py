"""API эндпоинты для устройств."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.api.deps import get_current_user, get_device_service_dep, get_subscription_service_dep
from app.core.exceptions import NotFoundException, BadRequestException
from app.models.device import Device
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas import DeviceResponse, DeviceCreate, DeviceBase
from app.services.device import DeviceService
from app.services.subscription import SubscriptionService

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=List[DeviceResponse])
async def get_devices(
    subscription_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
    device_service: DeviceService = Depends(get_device_service_dep),
) -> List[DeviceResponse]:
    """Получение устройств пользователя."""
    # Если subscription_id не указан, получаем активную подписку
    if subscription_id is None:
        subscription = await subscription_service.get_active_by_user(
            current_user.telegram_id
        )
        if not subscription:
            return []
        subscription_id = subscription.id
    else:
        subscription = await subscription_service.get_by_id(subscription_id)
        if not subscription:
            raise NotFoundException("Подписка не найдена")

        # Проверяем принадлежность
        if subscription.user_telegram_id != current_user.telegram_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Доступ запрещён",
            )

    devices = await device_service.get_by_subscription(subscription_id)
    return [DeviceResponse.model_validate(d) for d in devices]


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def add_device(
    device_data: DeviceBase,
    subscription_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
    device_service: DeviceService = Depends(get_device_service_dep),
) -> DeviceResponse:
    """Добавление устройства."""
    # Получаем подписку
    if subscription_id is None:
        subscription = await subscription_service.get_active_by_user(
            current_user.telegram_id
        )
        if not subscription:
            raise NotFoundException("Активная подписка не найдена")
    else:
        subscription = await subscription_service.get_by_id(subscription_id)
        if not subscription:
            raise NotFoundException("Подписка не найдена")

    # Проверяем принадлежность
    if subscription.user_telegram_id != current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    # Проверяем возможность добавления
    can_add = await device_service.can_add_device(subscription)
    if not can_add:
        raise BadRequestException(
            f"Достигнут лимит устройств: {subscription.device_limit}"
        )

    device = await device_service.add(subscription, device_data.name)
    logger.info(
        f"Пользователь {current_user.telegram_id} добавил устройство {device.id}"
    )

    return DeviceResponse.model_validate(device)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_device(
    device_id: int,
    subscription_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
    device_service: DeviceService = Depends(get_device_service_dep),
) -> None:
    """Удаление устройства."""
    # Получаем подписку
    if subscription_id is None:
        subscription = await subscription_service.get_active_by_user(
            current_user.telegram_id
        )
        if not subscription:
            raise NotFoundException("Активная подписка не найдена")
    else:
        subscription = await subscription_service.get_by_id(subscription_id)
        if not subscription:
            raise NotFoundException("Подписка не найдена")

    # Проверяем принадлежность
    if subscription.user_telegram_id != current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    # Получаем устройство
    device = await device_service.get_by_id(device_id)
    if not device:
        raise NotFoundException("Устройство не найдено")

    # Проверяем принадлежность устройства
    if device.subscription_id != subscription.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    await device_service.remove(subscription, device)
    logger.info(
        f"Пользователь {current_user.telegram_id} удалил устройство {device_id}"
    )


@router.post("/reset", status_code=status.HTTP_204_NO_CONTENT)
async def reset_devices(
    subscription_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service_dep),
    device_service: DeviceService = Depends(get_device_service_dep),
) -> None:
    """Сброс всех устройств."""
    # Получаем подписку
    if subscription_id is None:
        subscription = await subscription_service.get_active_by_user(
            current_user.telegram_id
        )
        if not subscription:
            raise NotFoundException("Активная подписка не найдена")
    else:
        subscription = await subscription_service.get_by_id(subscription_id)
        if not subscription:
            raise NotFoundException("Подписка не найдена")

    # Проверяем принадлежность
    if subscription.user_telegram_id != current_user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    await device_service.reset(subscription)
    logger.info(f"Пользователь {current_user.telegram_id} сбросил устройства")
