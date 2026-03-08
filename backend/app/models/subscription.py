"""Модель подписки."""

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    ARRAY,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseSQL, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class SubscriptionStatus(str, PyEnum):
    """Статус подписки."""

    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    TRIAL = "trial"
    PENDING = "pending"


class TrafficLimitStrategy(str, PyEnum):
    """Стратегия ограничения трафика."""

    MONTHLY = "monthly"
    TOTAL = "total"
    UNLIMITED = "unlimited"


class Subscription(BaseSQL, TimestampMixin):
    """Молель подписки."""

    __tablename__ = "subscriptions"

    # ID пользователя в RemnaWave
    user_remna_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    # ID пользователя в Telegram
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"),
        nullable=False,
        index=True,
    )

    # Статус и тип
    status: Mapped[SubscriptionStatus] = mapped_column(
        SQLEnum(SubscriptionStatus),
        default=SubscriptionStatus.PENDING,
        nullable=False,
        index=True,
    )
    is_trial: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Лимиты
    traffic_limit: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    device_limit: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    traffic_limit_strategy: Mapped[TrafficLimitStrategy] = mapped_column(
        SQLEnum(TrafficLimitStrategy),
        default=TrafficLimitStrategy.MONTHLY,
        nullable=False,
    )

    # Дополнительная информация
    tag: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    internal_squads: Mapped[List[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        default=list,
        nullable=False,
    )
    external_squad: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    # Срок действия
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # URL подписки
    url: Mapped[str] = mapped_column(String(1024), nullable=False)

    # Снимок плана (JSON)
    plan_snapshot: Mapped[dict] = mapped_column(
        default=dict,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="subscriptions",
        foreign_keys=[user_telegram_id],
    )

    def __repr__(self) -> str:
        return f"<Subscription {self.id} (user: {self.user_telegram_id})>"

    @property
    def is_active(self) -> bool:
        """Проверка активности подписки."""
        return self.status == SubscriptionStatus.ACTIVE

    @property
    def days_left(self) -> int:
        """Количество дней до истечения."""
        from datetime import timezone

        now = datetime.now(timezone.utc)
        delta = self.expire_at - now
        return max(0, delta.days)
