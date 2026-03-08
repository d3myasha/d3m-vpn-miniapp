"""API роутер v1."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, user, subscription, device, plan

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(subscription.router)
api_router.include_router(device.router)
api_router.include_router(plan.router)
