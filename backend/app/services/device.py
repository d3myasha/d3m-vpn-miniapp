"""Сервис для работы с устройствами."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.models.subscription import Subscription
from app.services.remnawave import RemnaWaveService


class DeviceService:
    """Сервис для работы с устройствами."""

    def __init__(self, session: AsyncSession, remnawave: RemnaWaveService):
        self.session = session
        self.remnawave = remnawave

    async def get_by_subscription(
        self,
        subscription_id: int,
    ) -> List[Device]:
        """Получение устройств подписки."""
        result = await self.session.execute(
            select(Device).where(Device.subscription_id == subscription_id)
        )
        return list(result.scalars().all())

    async def get_by_id(
        self,
        device_id: int,
    ) -> Optional[Device]:
        """Получение устройства по ID."""
        result = await self.session.execute(
            select(Device).where(Device.id == device_id)
        )
        return result.scalar_one_or_none()

    async def add(
        self,
        subscription: Subscription,
        device_name: str,
    ) -> Device:
        """Добавление устройства."""
        # Добавляем в RemnaWave
        remnawave_data = await self.remnawave.add_device(
            subscription_id=subscription.id,
            device_name=device_name,
        )

        # Создаём локальную запись
        device = Device(
            subscription_id=subscription.id,
            name=device_name,
            device_id=UUID(remnawave_data["id"]),
            is_active=remnawave_data.get("isActive", True),
        )
        self.session.add(device)
        await self.session.flush()
        return device

    async def remove(
        self,
        subscription: Subscription,
        device: Device,
    ) -> bool:
        """Удаление устройства."""
        # Удаляем из RemnaWave
        await self.remnawave.remove_device(
            subscription_id=subscription.id,
            device_id=device.device_id,
        )

        # Удаляем локальную запись
        await self.session.delete(device)
        await self.session.flush()
        return True

    async def reset(
        self,
        subscription: Subscription,
    ) -> bool:
        """Сброс всех устройств подписки."""
        # Сбрасываем в RemnaWave
        await self.remnawave.reset_devices(subscription_id=subscription.id)

        # Помечаем все локальные устройства как неактивные
        devices = await self.get_by_subscription(subscription.id)
        for device in devices:
            device.is_active = False

        await self.session.flush()
        return True

    async def can_add_device(
        self,
        subscription: Subscription,
    ) -> bool:
        """Проверка возможности добавления устройства."""
        devices = await self.get_by_subscription(subscription.id)
        active_devices = [d for d in devices if d.is_active]
        return len(active_devices) < subscription.device_limit


async def get_device_service(
    session: AsyncSession,
    remnawave: RemnaWaveService,
) -> DeviceService:
    """Получение сервиса устройств."""
    return DeviceService(session, remnawave)
