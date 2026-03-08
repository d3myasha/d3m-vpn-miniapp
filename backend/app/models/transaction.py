"""Модель транзакции."""

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    DECIMAL,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseSQL, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class TransactionStatus(str, PyEnum):
    """Статус транзакции."""

    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PurchaseType(str, PyEnum):
    """Тип покупки."""

    SUBSCRIPTION = "subscription"
    RENEWAL = "renewal"
    EXTENSION = "extension"


class PaymentGatewayType(str, PyEnum):
    """Тип платёжного шлюза."""

    TELEGRAM_STARS = "telegram_stars"
    YOOKASSA = "yookassa"
    YOOMONEY = "yoomoney"
    CRYPTOMUS = "cryptomus"
    HELEKET = "heleket"
    CRYPTOPAY = "cryptopay"
    ROBOKASSA = "robokassa"


class Currency(str, PyEnum):
    """Валюта."""

    RUB = "rub"
    USD = "usd"
    EUR = "eur"
    KZT = "kzt"
    UAH = "uah"
    BYN = "byn"
    GEL = "gel"
    TRY = "try"
    AED = "aed"


class Transaction(BaseSQL, TimestampMixin):
    """Модель транзакции."""

    __tablename__ = "transactions"

    # ID платежа
    payment_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
    )

    # ID пользователя
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"),
        nullable=False,
        index=True,
    )

    # Статус и тип
    status: Mapped[TransactionStatus] = mapped_column(
        SQLEnum(TransactionStatus),
        default=TransactionStatus.PENDING,
        nullable=False,
        index=True,
    )
    is_test: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    purchase_type: Mapped[PurchaseType] = mapped_column(
        SQLEnum(PurchaseType),
        nullable=False,
    )
    gateway_type: Mapped[PaymentGatewayType] = mapped_column(
        SQLEnum(PaymentGatewayType),
        nullable=False,
    )

    # Детали оплаты
    pricing: Mapped[dict] = mapped_column(default=dict, nullable=False)
    currency: Mapped[Currency] = mapped_column(
        SQLEnum(Currency),
        default=Currency.RUB,
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False,
    )

    # План (снимок)
    plan_snapshot: Mapped[dict] = mapped_column(default=dict, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        backref="transactions",
        foreign_keys=[user_telegram_id],
    )

    def __repr__(self) -> str:
        return f"<Transaction {self.payment_id} (user: {self.user_telegram_id})>"
