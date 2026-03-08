"""API эндпоинты для пользователей."""

from typing import List

from fastapi import APIRouter, Depends, status
from loguru import logger

from app.api.deps import get_current_user, get_user_service_dep
from app.models.user import User
from app.schemas import UserResponse, UserUpdate, ReferralStats
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Получение профиля текущего пользователя."""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service_dep),
) -> UserResponse:
    """Обновление профиля пользователя."""
    user = await user_service.update(current_user, user_data)
    logger.info(f"Пользователь {current_user.telegram_id} обновил профиль")
    return UserResponse.model_validate(user)


@router.get("/me/referrals", response_model=ReferralStats)
async def get_referral_stats(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service_dep),
) -> ReferralStats:
    """Получение статистики рефералов."""
    stats = await user_service.get_referral_stats(current_user.id)

    return ReferralStats(
        total_referrals=stats.get("total_referrals", 0),
        paid_referrals=0,  # TODO: реализовать подсчёт
        total_bonus_days=0,
        total_bonus_traffic=0,
        referral_code=current_user.referral_code,
        referral_link=f"https://t.me/{settings.bot_support_username}?start=ref_{current_user.referral_code}",
    )


@router.get("/me/referrals/list", response_model=List[UserResponse])
async def get_referrals_list(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service_dep),
) -> List[UserResponse]:
    """Получение списка рефералов."""
    referrals = await user_service.get_referrals(current_user.id)
    return [UserResponse.model_validate(r) for r in referrals]
