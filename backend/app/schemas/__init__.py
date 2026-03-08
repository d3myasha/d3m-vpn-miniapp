"""Pydantic схемы."""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# === User Schemas ===

class UserBase(BaseModel):
    """Базовая схема пользователя."""

    username: Optional[str] = None
    name: str
    language: str = "ru"


class UserCreate(UserBase):
    """Схема создания пользователя."""

    telegram_id: int
    referral_code: str


class UserUpdate(BaseModel):
    """Схема обновления пользователя."""

    username: Optional[str] = None
    name: Optional[str] = None
    language: Optional[str] = None


class UserResponse(UserBase):
    """Схема ответа пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    role: str
    points: int
    personal_discount: int
    purchase_discount: int
    is_blocked: bool
    is_rules_accepted: bool
    current_subscription_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# === Subscription Schemas ===

class SubscriptionBase(BaseModel):
    """Базовая схема подписки."""

    status: str
    is_trial: bool = False
    traffic_limit: int = 0
    device_limit: int = 1
    traffic_limit_strategy: str = "monthly"


class SubscriptionCreate(SubscriptionBase):
    """Схема создания подписки."""

    user_remna_id: UUID
    user_telegram_id: int
    expire_at: datetime
    url: str


class SubscriptionResponse(SubscriptionBase):
    """Схема ответа подписки."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_remna_id: UUID
    user_telegram_id: int
    tag: Optional[str] = None
    internal_squads: List[UUID] = []
    external_squad: Optional[UUID] = None
    expire_at: datetime
    url: str
    plan_snapshot: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    days_left: int = 0


# === Transaction Schemas ===

class TransactionBase(BaseModel):
    """Базовая схема транзакции."""

    status: str
    is_test: bool = False
    purchase_type: str
    gateway_type: str
    currency: str
    amount: Decimal


class TransactionResponse(TransactionBase):
    """Схема ответа транзакции."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    payment_id: UUID
    user_telegram_id: int
    pricing: Dict[str, Any] = {}
    plan_snapshot: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime


# === Plan Schemas ===

class PlanPriceSchema(BaseModel):
    """Схема цены плана."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    currency: str
    price: Decimal


class PlanDurationSchema(BaseModel):
    """Схема длительности плана."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    days: int
    prices: List[PlanPriceSchema] = []


class PlanBase(BaseModel):
    """Базовая схема плана."""

    name: str
    description: Optional[str] = None
    type: str = "standard"
    availability: str = "public"
    traffic_limit: int = 0
    device_limit: int = 1
    traffic_limit_strategy: str = "monthly"


class PlanResponse(PlanBase):
    """Схема ответа плана."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_index: int = 0
    is_active: bool = True
    tag: Optional[str] = None
    durations: List[PlanDurationSchema] = []
    created_at: datetime
    updated_at: datetime


# === Device Schemas ===

class DeviceBase(BaseModel):
    """Базовая схема устройства."""

    name: str


class DeviceCreate(DeviceBase):
    """Схема создания устройства."""

    subscription_id: int


class DeviceResponse(DeviceBase):
    """Схема ответа устройства."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    subscription_id: int
    device_id: UUID
    is_active: bool = True
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# === Promocode Schemas ===

class PromocodeBase(BaseModel):
    """Базовая схема промокода."""

    code: str
    type: str
    value: int


class PromocodeActivate(BaseModel):
    """Схема активации промокода."""

    code: str


class PromocodeResponse(PromocodeBase):
    """Схема ответа промокода."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool = True
    max_uses: Optional[int] = None
    uses_count: int = 0
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# === Referral Schemas ===

class ReferralResponse(BaseModel):
    """Схема ответа реферала."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    referrer_id: int
    referred_id: int
    bonus_days: int = 0
    bonus_traffic: int = 0
    is_paid: bool = False
    paid_at: Optional[datetime] = None
    created_at: datetime


class ReferralStats(BaseModel):
    """Статистика рефералов."""

    total_referrals: int = 0
    paid_referrals: int = 0
    total_bonus_days: int = 0
    total_bonus_traffic: int = 0
    referral_code: str
    referral_link: str


# === Auth Schemas ===

class TelegramInitData(BaseModel):
    """Данные инициализации Telegram."""

    user: Dict[str, Any]
    auth_date: int
    hash: str
    query_id: Optional[str] = None
    start_param: Optional[str] = None


class TokenResponse(BaseModel):
    """Ответ с токеном."""

    access_token: str
    token_type: str = "bearer"


# === Response wrappers ===

class SuccessResponse(BaseModel):
    """Успешный ответ."""

    success: bool = True
    message: str = "Операция выполнена успешно"


class ErrorResponse(BaseModel):
    """Ответ с ошибкой."""

    success: bool = False
    error: str
