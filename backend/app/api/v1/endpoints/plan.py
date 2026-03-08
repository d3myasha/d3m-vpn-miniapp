"""API эндпоинты для тарифных планов."""

from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_plan_service_dep
from app.models.plan import Plan
from app.models.user import User
from app.schemas import PlanResponse
from app.services.plan import PlanService

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("", response_model=List[PlanResponse])
async def get_plans(
    current_user: User = Depends(get_current_user),
    plan_service: PlanService = Depends(get_plan_service_dep),
) -> List[PlanResponse]:
    """Получение всех доступных тарифных планов."""
    plans = await plan_service.get_available_for_user(current_user.telegram_id)
    return [PlanResponse.model_validate(p) for p in plans]


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    plan_service: PlanService = Depends(get_plan_service_dep),
) -> PlanResponse:
    """Получение тарифного плана по ID."""
    plan = await plan_service.get_by_id(plan_id)
    return PlanResponse.model_validate(plan)
