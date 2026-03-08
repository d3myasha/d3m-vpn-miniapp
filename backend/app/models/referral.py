"""Модель реферала."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseSQL, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Referral(BaseSQL, TimestampMixin):
    """Модель реферала."""

    __tablename__ = "referrals"

    # ID пригласившего
    referrer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # ID приглашённого
    referred_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # Бонусы
    bonus_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bonus_traffic: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Статус выплаты
    is_paid: Mapped[bool] = mapped_column(default=False, nullable=False)
    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Referral {self.referrer_id} -> {self.referred_id}>"
