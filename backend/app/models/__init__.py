"""Модели базы данных."""

from app.models.base import BaseSQL, TimestampMixin
from app.models.device import Device
from app.models.plan import Plan, PlanDuration, PlanPrice
from app.models.promocode import Promocode, PromocodeType
from app.models.referral import Referral
from app.models.subscription import Subscription, SubscriptionStatus, TrafficLimitStrategy
from app.models.transaction import (
    Transaction,
    TransactionStatus,
    PurchaseType,
    PaymentGatewayType,
    Currency,
)
from app.models.user import User, UserRole

__all__ = [
    # Base
    "BaseSQL",
    "TimestampMixin",
    # Models
    "User",
    "Subscription",
    "Transaction",
    "Plan",
    "PlanDuration",
    "PlanPrice",
    "Device",
    "Promocode",
    "PromocodeType",
    "Referral",
    # Enums
    "UserRole",
    "SubscriptionStatus",
    "TrafficLimitStrategy",
    "TransactionStatus",
    "PurchaseType",
    "PaymentGatewayType",
    "Currency",
]
