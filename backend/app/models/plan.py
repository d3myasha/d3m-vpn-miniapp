"""Модель тарифного плана."""

import uuid
from typing import List, Optional

from sqlalchemy import (
    ARRAY,
    Boolean,
    DECIMAL,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseSQL, TimestampMixin


class PlanType(str):
    """Тип плана."""

    STANDARD = "standard"
    TRIAL = "trial"
    CUSTOM = "custom"


class PlanAvailability(str):
    """Доступность плана."""

    PUBLIC = "public"
    PRIVATE = "private"
    INVITE_ONLY = "invite_only"


class TrafficLimitStrategy(str):
    """Стратегия ограничения трафика."""

    MONTHLY = "monthly"
    TOTAL = "total"
    UNLIMITED = "unlimited"


class Plan(BaseSQL, TimestampMixin):
    """Модель тарифного плана."""

    __tablename__ = "plans"

    # Порядок отображения
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Статус
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Тип и доступность
    type: Mapped[PlanType] = mapped_column(
        SQLEnum(PlanType),
        default=PlanType.STANDARD,
        nullable=False,
    )
    availability: Mapped[PlanAvailability] = mapped_column(
        SQLEnum(PlanAvailability),
        default=PlanAvailability.PUBLIC,
        nullable=False,
    )

    # Информация
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Лимиты
    traffic_limit: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    device_limit: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    traffic_limit_strategy: Mapped[TrafficLimitStrategy] = mapped_column(
        SQLEnum(TrafficLimitStrategy),
        default=TrafficLimitStrategy.MONTHLY,
        nullable=False,
    )

    # Доступ для пользователей
    allowed_user_ids: Mapped[List[int]] = mapped_column(
        ARRAY(Integer),
        default=list,
        nullable=False,
    )

    # Squads
    internal_squads: Mapped[List[uuid.UUID]] = mapped_column(
        ARRAY(PG_UUID(as_uuid=True)),
        default=list,
        nullable=False,
    )
    external_squad: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )

    # Relationships
    durations: Mapped[List["PlanDuration"]] = relationship(
        "PlanDuration",
        back_populates="plan",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Plan {self.name}>"


class PlanDuration(BaseSQL, TimestampMixin):
    """Модель длительности плана."""

    __tablename__ = "plan_durations"

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete="CASCADE"),
        nullable=False,
    )
    days: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    plan: Mapped[Plan] = relationship("Plan", back_populates="durations")
    prices: Mapped[List["PlanPrice"]] = relationship(
        "PlanPrice",
        back_populates="plan_duration",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<PlanDuration {self.days} days>"


class PlanPrice(BaseSQL, TimestampMixin):
    """Модель цены плана."""

    __tablename__ = "plan_prices"

    plan_duration_id: Mapped[int] = mapped_column(
        ForeignKey("plan_durations.id", ondelete="CASCADE"),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)

    # Relationships
    plan_duration: Mapped[PlanDuration] = relationship(
        "PlanDuration",
        back_populates="prices",
    )

    def __repr__(self) -> str:
        return f"<PlanPrice {self.price} {self.currency}>"
