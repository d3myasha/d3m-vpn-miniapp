"""Модель промокода."""

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import (
    ARRAY,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseSQL, TimestampMixin


class PromocodeType(str, PyEnum):
    """Тип промокода."""

    DISCOUNT = "discount"
    DAYS = "days"
    TRAFFIC = "traffic"
    ACTIVATION = "activation"


class Promocode(BaseSQL, TimestampMixin):
    """Модель промокода."""

    __tablename__ = "promocodes"

    # Код
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Тип
    type: Mapped[PromocodeType] = mapped_column(
        SQLEnum(PromocodeType),
        nullable=False,
    )

    # Значение
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    # Статус
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Ограничения
    max_uses: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    uses_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Срок действия
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # План (для активации)
    plan_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("plans.id"),
        nullable=True,
    )

    # Relationships
    plan: Mapped[Optional["Plan"]] = relationship("Plan")

    def __repr__(self) -> str:
        return f"<Promocode {self.code}>"

    @property
    def is_expired(self) -> bool:
        """Проверка истечения срока."""
        from datetime import timezone

        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def can_use(self) -> bool:
        """Можно ли использовать."""
        if not self.is_active:
            return False
        if self.is_expired:
            return False
        if self.max_uses is not None and self.uses_count >= self.max_uses:
            return False
        return True
