"""Сервис для работы с подписками."""

from datetime import datetime, timedelta, timezone
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscription import Subscription, SubscriptionStatus
from app.models.user import User
from app.services.remnawave import RemnaWaveService


class SubscriptionService:
    """Сервис для работы с подписками."""

    def __init__(self, session: AsyncSession, remnawave: RemnaWaveService):
        self.session = session
        self.remnawave = remnawave

    async def get_by_id(
        self,
        subscription_id: int,
    ) -> Optional[Subscription]:
        """Получение подписки по ID."""
        result = await self.session.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_telegram_id(
        self,
        telegram_id: int,
    ) -> List[Subscription]:
        """Получение всех подписок пользователя."""
        result = await self.session.execute(
            select(Subscription)
            .where(Subscription.user_telegram_id == telegram_id)
            .order_by(Subscription.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_active_by_user(
        self,
        telegram_id: int,
    ) -> Optional[Subscription]:
        """Получение активной подписки пользователя."""
        result = await self.session.execute(
            select(Subscription).where(
                Subscription.user_telegram_id == telegram_id,
                Subscription.status == SubscriptionStatus.ACTIVE,
            )
        )
        return result.scalar_one_or_none()

    async def create_from_remnawave(
        self,
        user: User,
        remnawave_data: dict,
    ) -> Subscription:
        """Создание подписки из данных RemnaWave."""
        subscription = Subscription(
            user_remna_id=UUID(remnawave_data["id"]),
            user_telegram_id=user.telegram_id,
            status=SubscriptionStatus(remnawave_data.get("status", "pending")),
            is_trial=remnawave_data.get("isTrial", False),
            traffic_limit=remnawave_data.get("trafficLimit", 0),
            device_limit=remnawave_data.get("deviceLimit", 1),
            traffic_limit_strategy=remnawave_data.get("trafficLimitStrategy", "monthly"),
            tag=remnawave_data.get("tag"),
            internal_squads=[
                UUID(s) for s in remnawave_data.get("internalSquads", [])
            ],
            external_squad=(
                UUID(remnawave_data["externalSquad"])
                if remnawave_data.get("externalSquad")
                else None
            ),
            expire_at=datetime.fromisoformat(remnawave_data["expireAt"].replace("Z", "+00:00")),
            url=remnawave_data.get("url", ""),
            plan_snapshot=remnawave_data.get("plan", {}),
        )
        self.session.add(subscription)
        await self.session.flush()

        # Обновляем текущую подписку пользователя
        user.current_subscription_id = subscription.id
        await self.session.flush()

        return subscription

    async def update_status(
        self,
        subscription: Subscription,
        status: SubscriptionStatus,
    ) -> Subscription:
        """Обновление статуса подписки."""
        subscription.status = status
        await self.session.flush()
        return subscription

    async def renew(
        self,
        subscription: Subscription,
        days: int,
    ) -> Subscription:
        """Продление подписки."""
        # Продлеваем в RemnaWave
        remnawave_data = await self.remnawave.renew_subscription(
            subscription_id=subscription.id,
            duration_days=days,
        )

        # Обновляем локальные данные
        subscription.expire_at = datetime.fromisoformat(
            remnawave_data["expireAt"].replace("Z", "+00:00")
        )
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.plan_snapshot = remnawave_data.get("plan", {})

        await self.session.flush()
        return subscription

    async def get_traffic_usage(
        self,
        subscription: Subscription,
    ) -> dict:
        """Получение использования трафика."""
        usage = await self.remnawave.get_traffic_usage(subscription.id)
        return {
            "used": usage.get("used", 0),
            "limit": subscription.traffic_limit,
            "remaining": max(0, subscription.traffic_limit - usage.get("used", 0)),
            "percentage": (
                (usage.get("used", 0) / subscription.traffic_limit * 100)
                if subscription.traffic_limit > 0
                else 0
            ),
        }

    async def sync_with_remnawave(
        self,
        subscription: Subscription,
    ) -> Optional[Subscription]:
        """Синхронизация подписки с RemnaWave."""
        remnawave_data = await self.remnawave.get_subscription(subscription.user_remna_id)

        if not remnawave_data:
            return None

        subscription.status = SubscriptionStatus(remnawave_data.get("status", "pending"))
        subscription.traffic_limit = remnawave_data.get("trafficLimit", 0)
        subscription.device_limit = remnawave_data.get("deviceLimit", 1)
        subscription.expire_at = datetime.fromisoformat(
            remnawave_data["expireAt"].replace("Z", "+00:00")
        )
        subscription.plan_snapshot = remnawave_data.get("plan", {})

        await self.session.flush()
        return subscription


async def get_subscription_service(
    session: AsyncSession,
    remnawave: RemnaWaveService,
) -> SubscriptionService:
    """Получение сервиса подписок."""
    return SubscriptionService(session, remnawave)
