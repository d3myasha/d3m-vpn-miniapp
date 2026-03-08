"""Сервис для работы с пользователями."""

import uuid
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas import UserCreate, UserUpdate


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(
        self,
        telegram_id: int,
    ) -> Optional[User]:
        """Получение пользователя по Telegram ID."""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        user_id: int,
    ) -> Optional[User]:
        """Получение пользователя по ID."""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        user_data: UserCreate,
        referred_by_id: Optional[int] = None,
    ) -> User:
        """Создание пользователя."""
        user = User(
            telegram_id=user_data.telegram_id,
            username=user_data.username,
            name=user_data.name,
            referral_code=user_data.referral_code,
            language=user_data.language,
            referred_by_id=referred_by_id,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(
        self,
        user: User,
        user_data: UserUpdate,
    ) -> User:
        """Обновление пользователя."""
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.session.flush()
        return user

    async def block(
        self,
        user: User,
    ) -> User:
        """Блокировка пользователя."""
        user.is_blocked = True
        await self.session.flush()
        return user

    async def unblock(
        self,
        user: User,
    ) -> User:
        """Разблокировка пользователя."""
        user.is_blocked = False
        await self.session.flush()
        return user

    async def add_points(
        self,
        user: User,
        points: int,
    ) -> User:
        """Добавление баллов пользователю."""
        user.points += points
        await self.session.flush()
        return user

    async def spend_points(
        self,
        user: User,
        points: int,
    ) -> bool:
        """Списание баллов у пользователя."""
        if user.points < points:
            return False
        user.points -= points
        await self.session.flush()
        return True

    async def get_referrals(
        self,
        user_id: int,
    ) -> List[User]:
        """Получение рефералов пользователя."""
        result = await self.session.execute(
            select(User).where(User.referred_by_id == user_id)
        )
        return list(result.scalars().all())

    async def get_referral_stats(
        self,
        user_id: int,
    ) -> dict:
        """Получение статистики рефералов."""
        result = await self.session.execute(
            select(
                func.count(User.id),
            ).where(User.referred_by_id == user_id)
        )
        total = result.scalar() or 0

        return {
            "total_referrals": total,
        }


async def get_user_service(session: AsyncSession) -> UserService:
    """Получение сервиса пользователя."""
    return UserService(session)
