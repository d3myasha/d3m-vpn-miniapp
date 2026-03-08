"""Модель пользователя."""

from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseSQL, TimestampMixin

if TYPE_CHECKING:
    from app.models.subscription import Subscription


class UserRole(str, PyEnum):
    """Роль пользователя."""

    USER = "user"
    ADMIN = "admin"
    DEVELOPER = "developer"


class User(BaseSQL, TimestampMixin):
    """Модель пользователя."""

    __tablename__ = "users"

    # Telegram данные
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Реферальная система
    referral_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    referred_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    # Профиль
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )
    language: Mapped[str] = mapped_column(String(10), default="ru", nullable=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_bot_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_rules_accepted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Баланс и скидки
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    personal_discount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    purchase_discount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Текущая подписка
    current_subscription_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("subscriptions.id"),
        nullable=True,
    )

    # Relationships
    current_subscription: Mapped[Optional["Subscription"]] = relationship(
        "Subscription",
        foreign_keys=[current_subscription_id],
        back_populates="user",
    )
    subscriptions: Mapped[List["Subscription"]] = relationship(
        "Subscription",
        back_populates="user",
        foreign_keys="Subscription.user_telegram_id",
    )
    referred_by: Mapped[Optional["User"]] = relationship(
        "User",
        remote_side="User.id",
        backref="referrals",
    )

    def __repr__(self) -> str:
        return f"<User {self.telegram_id} ({self.username})>"
