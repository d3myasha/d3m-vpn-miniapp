"""Сервис для работы с тарифными планами."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import Plan, PlanDuration, PlanPrice
from app.services.remnawave import RemnaWaveService


class PlanService:
    """Сервис для работы с тарифными планами."""

    def __init__(self, session: AsyncSession, remnawave: RemnaWaveService):
        self.session = session
        self.remnawave = remnawave

    async def get_all(
        self,
        active_only: bool = True,
    ) -> List[Plan]:
        """Получение всех планов."""
        query = select(Plan)
        if active_only:
            query = query.where(Plan.is_active == True)
        query = query.order_by(Plan.order_index)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(
        self,
        plan_id: int,
    ) -> Optional[Plan]:
        """Получение плана по ID."""
        result = await self.session.execute(
            select(Plan).where(Plan.id == plan_id)
        )
        return result.scalar_one_or_none()

    async def get_available_for_user(
        self,
        telegram_id: int,
    ) -> List[Plan]:
        """Получение доступных планов для пользователя."""
        result = await self.session.execute(
            select(Plan).where(
                Plan.is_active == True,
                Plan.availability == "public",
            )
        )
        return list(result.scalars().all())

    async def sync_with_remnawave(self) -> int:
        """Синхронизация планов с RemnaWave."""
        remnawave_plans = await self.remnawave.get_plans()

        created_count = 0
        for rw_plan in remnawave_plans:
            # Проверяем существование
            existing = await self.get_by_id(rw_plan["id"])

            if not existing:
                # Создаём новый план
                plan = Plan(
                    id=rw_plan["id"],
                    name=rw_plan["name"],
                    description=rw_plan.get("description"),
                    type=rw_plan.get("type", "standard"),
                    availability=rw_plan.get("availability", "public"),
                    traffic_limit=rw_plan.get("trafficLimit", 0),
                    device_limit=rw_plan.get("deviceLimit", 1),
                    traffic_limit_strategy=rw_plan.get("trafficLimitStrategy", "monthly"),
                    is_active=rw_plan.get("isActive", True),
                    order_index=rw_plan.get("orderIndex", 0),
                )
                self.session.add(plan)
                created_count += 1

        await self.session.flush()
        return created_count


async def get_plan_service(
    session: AsyncSession,
    remnawave: RemnaWaveService,
) -> PlanService:
    """Получение сервиса планов."""
    return PlanService(session, remnawave)
